from typing import Tuple, List
from .stack import Stack
from .block import Block
from queue import Queue

class SimulationAction:
    """Base class for actions in the simulation.
    SimulationActions are created from SimulationInputs (by the input processor only!),
    when the SimulationInput is valid and executable."""
    def __init__(self, reply_queue: Queue):
        self._reply_queue: Queue = reply_queue

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
    """Action for stopping the simulation."""
    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def _get_simulation_status(self, stacks: List [Stack], robot):
        status = {
            "stacks_status": [stack.to_dict() for stack in stacks],
            "robot_status": robot.to_dict()
        }
        return status

    def reply_success(self, stacks: List[Stack], robot):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, self._get_simulation_status(stacks, robot)))


class RobotAction(SimulationAction):
    """Base class for robot actions in the simulation."""
    def __init__(self, reply_queue: Queue, block: Block, stack: Stack):
        super().__init__(reply_queue)
        self._block = block
        self._stack = stack

    def get_block(self) -> Block:
        return self._block

    def get_stack(self) -> Stack:
        return self._stack
    
    def get_target(self) -> Tuple[int, int]:
        """Get the target position for the action. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_target method")


class PickUpAction(RobotAction):
    """Action for picking up a block."""
    def __init__(self, reply_queue: Queue, block: Block, stack: Stack):
        super().__init__(reply_queue, block, stack)

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} picked up successfully from stack {self._stack.get_number()}"))

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y())


class PutDownAction(RobotAction):
    """Action for putting down a block."""
    def __init__(self, reply_queue: Queue, block: Block, stack: Stack):
        super().__init__(reply_queue, block, stack)

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} put down successfully on stack {self._stack.get_number()}"))

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y() - self._block.get_size()[1])


class StackAction(RobotAction):
    """Action for stacking a block on another block."""
    def __init__(self, reply_queue: Queue, block: Block, stack: Stack, target_block: Block):
        super().__init__(reply_queue, block, stack)
        self._target_block = target_block

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} stacked successfully on block {self._target_block.get_name()} in stack {self._stack.get_number()}"))

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y() - self._block.get_size()[1])


class UnstackAction(RobotAction):
    """Action for unstacking a block from another block."""
    def __init__(self, reply_queue: Queue, block: Block, stack: Stack, block_below: Block):
        super().__init__(reply_queue, block, stack)
        self._block_below = block_below

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, f"Block {self._block.get_name()} unstacked successfully from block {self._block_below.get_name()} in stack {self._stack.get_number()}"))

    def get_target(self) -> Tuple[int, int]:
        return (self._stack.get_x(), self._stack.get_top_y())

