from typing import Optional, List, Union
from queue import Queue


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


class QuitInput(SimulationInput):
    """Input for quitting the application."""
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)


class StartInput(SimulationInput):
    """Input for starting the simulation."""
    def __init__(self, reply_queue: Queue, stack_config = None):
        super().__init__(reply_queue)
        self._stack_config = stack_config

    def get_stack_config(self):
        """Get the stack configuration for the simulation"""
        return self._stack_config


class StopInput(SimulationInput):
    """Input for stopping the simulation."""
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)


class GetStatusInput(SimulationInput):
    """Input for getting the status of the simulation."""
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)


class PickUpInput(SimulationInput):
    """Input for picking up a block."""
    def __init__(self, reply_queue: Queue, block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name

    def get_block_name(self) -> str:
        """Get the name of the block to pick up"""
        return self._block_name


class PutDownInput(SimulationInput):
    """Input for putting down a block."""
    def __init__(self, reply_queue: Queue, block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name

    def get_block_name(self) -> str:
        """Get the name of the block to put down"""
        return self._block_name


class StackInput(SimulationInput):
    """Input for stacking a block on another block."""
    def __init__(self, reply_queue: Queue, block_name: str, target_block_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._target_block_name = target_block_name

    def get_block_name(self) -> str:
        """Get the name of the block being stacked"""
        return self._block_name

    def get_target_block_name(self) -> str:
        """Get the name of the target block on which the block is being stacked"""
        return self._target_block_name


class UnstackInput(SimulationInput):
    """Input for unstacking a block from another block."""
    def __init__(self, reply_queue: Queue, block_name: str, block_below_name: str):
        super().__init__(reply_queue)
        self._block_name = block_name
        self._block_below_name = block_below_name
    
    def get_block_name(self) -> str:
        """Get the name of the block being unstacked"""
        return self._block_name

    def get_block_below_name(self) -> str:
        """Get the name of the block below which is being unstacked"""
        return self._block_below_name