from typing import Tuple
from .stack import Stack
from .block import Block
from queue import Queue
from abc import ABC, abstractmethod

class SimulationAction(ABC):
    """Base class for actions in the simulation.
    Actions can be created by user input or by the API.
    They are created in an unvalidated state and then validated by the constraint manager."""

    def __init__(self, reply_queue: Queue):
        self._reply_queue: Queue = reply_queue
        self._is_valid: bool | None = None

    def is_valid(self) -> bool | None:
        """Check if the action has been validated. Returns True if valid, False if invalid, None if not yet validated."""
        return self._is_valid
    
    def set_valid(self):
        """Mark the action as validated"""
        self._is_valid = True

    def set_invalid(self, invalid_reason: str):
        """Mark the action as invalidated"""
        self._is_valid = False
        self._reply_queue.put((False, self._failure_message() + " - " + invalid_reason))

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, self._success_message()))

    @abstractmethod
    def _success_message(self) -> str:
        """Defines the success message to be sent back to the reply queue if action was successfully executed.
        Must be implemented by subclasses to send a success reply"""
        pass

    @abstractmethod
    def _failure_message(self) -> str:
        """Defines the failure message to be sent back to the reply queue if action was not successfully executed.
        Must be implemented by subclasses to send a failure reply"""
        pass


class QuitAction(SimulationAction):
    """Action for quitting the application."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def _success_message(self):
        return "Application is quitting"

    def _failure_message(self) -> str:
        return "Application could not be quit"


class StartAction(SimulationAction):
    """Action for starting the simulation."""

    def __init__(self, reply_queue: Queue, stack_config=None, scenario_id=None, constraint_set=None):
        super().__init__(reply_queue)
        self._stack_config = stack_config
        self._scenario_id = scenario_id
        self._constraint_set = constraint_set

    def get_stack_config(self):
        """Get the stack configuration for the simulation"""
        return self._stack_config
    
    def get_scenario_id(self):
        """Get the scenario ID for the simulation"""
        return self._scenario_id
    
    def get_constraint_set(self):
        """Get the constraint set name for the simulation"""
        return self._constraint_set
    
    def _success_message(self):
        config_str = f"given stack config: {self._stack_config}" if self._stack_config is not None else "random stacks"
        return f"Simulation started with {config_str}"

    def _failure_message(self) -> str:
        return "Simulation could not be started"
    

class PreStartAction(SimulationAction):
    """Action for changing the constraint set before starting the simulation with a StartAction."""

    def __init__(self, reply_queue: Queue, stack_config=None, scenario_id=None, constraint_set=None):
        super().__init__(reply_queue)
        self._stack_config = stack_config
        self._scenario_id = scenario_id
        self._constraint_set = constraint_set
    
    def get_constraint_set(self) -> str | None:
        """Get the new constraint set to be applied."""
        return self._constraint_set

    def set_constraint_set(self, constraint_set: str):
        """Set the new constraint set to be applied."""
        self._constraint_set = constraint_set

    def get_scenario_id(self) -> str | None:
        """Get the scenario ID for the simulation"""
        return self._scenario_id
    
    def get_stack_config(self):
        """Get the initial stacks for the simulation"""
        return self._stack_config
    
    def set_stack_config(self, stack_config):
        """Set the initial stacks for the simulation"""
        self._stack_config = stack_config

    def create_start_action(self) -> StartAction:
        """Create a StartAction with the current parameters."""
        return StartAction(
            reply_queue=self._reply_queue,
            stack_config=self._stack_config,
            scenario_id=self._scenario_id,
            constraint_set=self._constraint_set
        )

    def _success_message(self):
        return f"Constraint set changed to {self._constraint_set}"

    def _failure_message(self) -> str:
        return "Constraint set could not be changed"


class StopAction(SimulationAction):
    """Action for stopping the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def _success_message(self):
        return "Simulation stopped"

    def _failure_message(self) -> str:
        return "Simulation could not be stopped"


class GetStatusAction(SimulationAction):
    """Action for getting the status of the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)
        self._status_dict: dict = None

    def set_status_dict(self, status_dict: dict):
        self._status_dict = status_dict

    def _success_message(self):
        status_string = str(self._status_dict)
        return status_string

    def _failure_message(self) -> str:
        return "Simulation status could not be retrieved"


class RobotAction(SimulationAction):
    """Base class for robot actions in the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)
    
    @abstractmethod
    def get_target(self) -> Tuple[int, int]:
        """Get the target position for the action. Must be implemented by subclasses."""
        pass


class PickUpAction(RobotAction):
    """Action for picking up a block."""

    def __init__(self, reply_queue: Queue, block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block: Block = None
        self._stack: Stack = None

    def get_block_name(self) -> str:
        """Get the name of the block to pick up"""
        return self._block_name

    def get_block(self) -> Block:
        """Get the block to be picked up"""
        return self._block

    def set_block(self, block: Block):
        """After verification of the block name being passed as a string, 
        this method can be used to set the block to be picked up."""
        self._block = block

    def get_stack(self) -> Stack:
        """Get the stack from which the block will be picked up"""
        return self._stack

    def set_stack(self, stack: Stack):
        """After verification of the block name being passed as a string, 
        this method can be used to set the stack from which the block will be picked up."""
        self._stack = stack

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y())

    def _success_message(self):
        return f"Block {self._block.get_name()} picked up successfully from stack {self._stack.get_number()}"

    def _failure_message(self) -> str:
        return "Block could not be picked up"


class PutDownAction(RobotAction):
    """Action for putting down a block."""

    def __init__(self, reply_queue: Queue, block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block: Block = None
        self._stack: Stack = None

    def get_block_name(self) -> str:
        """Get the name of the block to put down"""
        return self._block_name
    
    def get_block(self) -> Block:
        """Get the block to be put down"""
        return self._block

    def set_block(self, block: Block):
        """After verification of the block name being passed as a string,
        this method can be used to set the block to be put down."""
        self._block = block

    def get_stack(self) -> Stack:
        """Get the stack on which the block will be put down"""
        return self._stack

    def set_stack(self, stack: Stack):
        """After verification that a free stack is available,
        this method can be used to set the stack on which the block will be put down."""
        self._stack = stack

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y() - self._block.get_size()[1])

    def _success_message(self):
        return f"Block {self._block.get_name()} put down successfully on stack {self._stack.get_number()}"
    
    def _failure_message(self) -> str:
        return "Block could not be put down"


class StackAction(RobotAction):
    """Action for stacking a block on another block."""

    def __init__(self, reply_queue: Queue, block_name: str, target_block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block: Block = None
        self._target_block_name = target_block_name
        self._target_block: Block = None
        self._stack: Stack = None

    def get_block_name(self) -> str:
        """Get the name of the block being stacked"""
        return self._block_name

    def get_block(self) -> Block:
        """Get the block being stacked"""
        return self._block

    def set_block(self, block: Block):
        """After verification of the block name being passed as a string,
        this method can be used to set the block to be stacked."""
        self._block = block

    def get_target_block_name(self) -> str:
        """Get the name of the target block on which the block is being stacked"""
        return self._target_block_name

    def get_target_block(self) -> Block:
        """Get the target block on which the block is being stacked"""
        return self._target_block

    def set_target_block(self, target_block: Block):
        """After verification of the target block name being passed as a string,
        this method can be used to set the target block on which the block will be stacked."""
        self._target_block = target_block

    def get_stack(self) -> Stack:
        """Get the stack on which the block will be stacked"""
        return self._stack

    def set_stack(self, stack: Stack):
        """After verification of the target block name being passed as a string,
        this method can be used to set the stack on which the block will be stacked."""
        self._stack = stack

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y() - self._block.get_size()[1])

    def _success_message(self):
        return f"Block {self._block.get_name()} stacked successfully on block {self._target_block.get_name()} in stack {self._stack.get_number()}"

    def _failure_message(self) -> str:
        return "Block could not be stacked"

class UnstackAction(RobotAction):
    """Action for unstacking a block from another block."""

    def __init__(self, reply_queue: Queue, block_name: str, block_below_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block: Block = None
        self._block_below_name = block_below_name
        self._block_below: Block = None
        self._stack: Stack = None

    def get_block_name(self) -> str:
        """Get the name of the block being unstacked"""
        return self._block_name

    def get_block(self) -> Block:
        """Get the block being unstacked"""
        return self._block
    
    def set_block(self, block: Block):
        """After verification of the block name being passed as a string,
        this method can be used to set the block to be unstacked."""
        self._block = block

    def get_block_below_name(self) -> str:
        """Get the name of the block below which is being unstacked"""
        return self._block_below_name

    def get_block_below(self) -> Block:
        """Get the block below which is being unstacked"""
        return self._block_below

    def set_block_below(self, block_below: Block):
        """After verification of the block below name being passed as a string,
        this method can be used to set the block below the block to be unstacked."""
        self._block_below = block_below

    def get_stack(self) -> Stack:
        """Get the stack from which the block will be unstacked"""
        return self._stack

    def set_stack(self, stack: Stack):
        """After verification of the block name being passed as a string,
        this method can be used to set the stack from which the block will be unstacked."""
        self._stack = stack

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y())
    
    def _success_message(self):
        return f"Block {self._block.get_name()} unstacked successfully from block {self._block_below.get_name()} in stack {self._stack.get_number()}"

    def _failure_message(self) -> str:
        return "Block could not be unstacked"