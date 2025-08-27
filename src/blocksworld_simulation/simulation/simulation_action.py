from typing import Tuple
from .stack import Stack
from .block import Block
from queue import Queue


class SimulationAction:
    """Base class for actions in the simulation.
    Actions can be created by user input or by the API.
    They are created in an unvalidated state and then validated by the input processor."""

    def __init__(self, reply_queue: Queue):
        self._reply_queue: Queue = reply_queue
        self._is_validated: bool = False

    def is_validated(self) -> bool:
        """Check if the action has been validated"""
        return self._is_validated
    
    def set_validated(self):
        """Mark the action as validated"""
        self._is_validated = True

    def reply(self, success: bool, message: str):
        """Send a reply back to the reply queue"""
        self._reply_queue.put((success, message))

    def reply_success(self):
        # must be implemented by subclasses to send a success reply
        raise NotImplementedError("Subclasses must implement reply_success method")


class QuitAction(SimulationAction):
    """Action for quitting the application."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, "Application is quitting"))


class StartAction(SimulationAction):
    """Action for starting the simulation."""

    def __init__(self, reply_queue: Queue, stack_config = None):
        super().__init__(reply_queue)
        self._stack_config = stack_config

    def get_stack_config(self):
        """Get the stack configuration for the simulation"""
        return self._stack_config
    
    def reply_success(self):
        """Send a success reply back to the reply queue"""
        config_str = f"given stack config: {self._stack_config}" if self._stack_config is not None else "random stacks"
        self._reply_queue.put((True, f"Simulation started with {config_str}"))


class StopAction(SimulationAction):
    """Action for stopping the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, "Simulation stopped"))

    
class GetStatusAction(SimulationAction):
    """Action for getting the status of the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def reply_success(self, status_dict: dict):
        """Send status dict back to reply queue"""
        self._reply_queue.put((True, status_dict))


class RobotAction(SimulationAction):
    """Base class for robot actions in the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)
    
    def get_target(self) -> Tuple[int, int]:
        """Get the target position for the action. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_target method")


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

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} picked up successfully from stack {self._stack.get_number()}"))


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

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} put down successfully on stack {self._stack.get_number()}"))


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

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} stacked successfully on block {self._target_block.get_name()} in stack {self._stack.get_number()}"))


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
    
    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} unstacked successfully from block {self._block_below.get_name()} in stack {self._stack.get_number()}"))