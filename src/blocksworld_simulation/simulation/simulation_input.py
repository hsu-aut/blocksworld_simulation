from typing import Optional, List, Union
from queue import Queue

from blocksworld_simulation.simulation.block import Block
from blocksworld_simulation.simulation.simulation_action import SimulationAction, QuitAction, StartAction, StopAction, GetStatusAction, PickUpAction, PutDownAction, StackAction, UnstackAction
from blocksworld_simulation.simulation.stack import Stack


class SimulationInput:
    """Base class for inputs to the simulation coming from the user via keyboard/mouse or via the REST API.
    Inputs are not validated (which will be done by the input processor).
    If denied, the reply queue (to the API or to the CLI, depending on the origin of the input) will be used to give feedback.
    If valid and executable, a SimulationAction will be created and executed."""
    
    def __init__(self, reply_queue: Queue):
        self._reply_queue = reply_queue
    
    def get_reply_queue(self) -> Queue:
        """Get the reply queue"""
        return self._reply_queue

    def reply(self, success: bool, message: str):
        """Send a reply back to the reply queue"""
        self._reply_queue.put((success, message))

    def create_action(self) -> SimulationAction:
        """Create a simulation action from self."""
        raise NotImplementedError("Subclasses must implement this method")


class QuitInput(SimulationInput):
    """Input for quitting the application."""
    
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def create_action(self) -> QuitAction:
        return QuitAction(self.get_reply_queue())


class StartInput(SimulationInput):
    """Input for starting the simulation."""
    
    def __init__(self, reply_queue: Queue, stack_config = None):
        super().__init__(reply_queue)
        self._stack_config = stack_config

    def get_stack_config(self):
        """Get the stack configuration for the simulation"""
        return self._stack_config
    
    def create_action(self) -> StartAction:
        return StartAction(self.get_reply_queue(), self.get_stack_config())


class StopInput(SimulationInput):
    """Input for stopping the simulation."""
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def create_action(self) -> StopAction:
        return StopAction(self.get_reply_queue())


class GetStatusInput(SimulationInput):
    """Input for getting the status of the simulation."""
    
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def create_action(self) -> GetStatusAction:
        return GetStatusAction(self.get_reply_queue())


class PickUpInput(SimulationInput):
    """Input for picking up a block."""
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

    def create_action(self) -> PickUpAction:
        return PickUpAction(self.get_reply_queue(), self._block, self._stack)


class PutDownInput(SimulationInput):
    """Input for putting down a block."""
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

    def create_action(self) -> PutDownAction:
        return PutDownAction(self.get_reply_queue(), self._block, self._stack)


class StackInput(SimulationInput):
    """Input for stacking a block on another block."""
    def __init__(self, reply_queue: Queue, block_name: str, target_block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._target_block_name = target_block_name
        self._block: Block = None
        self._stack: Stack = None
        self._target_block: Block = None

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

    def create_action(self) -> StackAction:
        return StackAction(self.get_reply_queue(), self._block, self._stack, self._target_block)


class UnstackInput(SimulationInput):
    """Input for unstacking a block from another block."""
    def __init__(self, reply_queue: Queue, block_name: str, block_below_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block_below_name = block_below_name
        self._block: Block = None
        self._stack: Stack = None
        self._block_below: Block = None

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

    def create_action(self) -> UnstackAction:
        return UnstackAction(self.get_reply_queue(), self._block, self._stack, self._block_below)