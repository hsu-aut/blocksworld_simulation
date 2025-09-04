from typing import Tuple
from .robot_action import RobotAction
from ..stack import Stack
from ..block import Block
from ...api.request_models import StackRequest
from ...api.request_models.execution_plan import StackStep


class StackAction(RobotAction):
    """Action for stacking a block on another block."""

    def __init__(self, data: StackRequest | StackStep):
        super().__init__()
        self._block_name = data.block1
        self._block: Block = None
        self._target_block_name = data.block2
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