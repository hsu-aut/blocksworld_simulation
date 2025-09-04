from typing import Tuple
from .robot_action import RobotAction
from ..stack import Stack
from ..block import Block
from ...api.request_models import PickUpRequest
from ...api.request_models.execution_plan import PickUpStep


class PickUpAction(RobotAction):
    """Action for picking up a block."""

    def __init__(self, data: PickUpRequest | PickUpStep):
        super().__init__()
        self._block_name = data.block
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