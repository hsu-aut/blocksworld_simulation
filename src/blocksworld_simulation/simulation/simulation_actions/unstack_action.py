from typing import Tuple
from queue import Queue
from .robot_action import RobotAction
from ..stack import Stack
from ..block import Block
from ...api.request_models import UnstackRequest


class UnstackAction(RobotAction):
    """Action for unstacking a block from another block."""

    def __init__(self, reply_queue: Queue, request: UnstackRequest):
        super().__init__(reply_queue)
        self._block_name = request.block1
        self._block: Block = None
        self._block_below_name = request.block2
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