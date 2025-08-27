from typing import Tuple
from .robot_action import RobotAction
from ..stack import Stack
from ..block import Block
from ...api.request_models import PutDownRequest


class PutDownAction(RobotAction):
    """Action for putting down a block."""

    def __init__(self, request: PutDownRequest):
        super().__init__()
        self._block_name = request.block
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