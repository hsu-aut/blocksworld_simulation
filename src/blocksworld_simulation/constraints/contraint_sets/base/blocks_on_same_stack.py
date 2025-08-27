from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import SimulationAction, UnstackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class BlocksOnSameStack(Constraint):
    """Constraint to check if two blocks are on the same stack."""

    def validate(self, state: SimulationState, action: UnstackAction) -> bool:
        block_name = action.get_block_name()
        block_below_name = action.get_block_below_name()
        stacks = state.get_stacks()
        # find the stacks in which both blocks are located
        block_stack = None
        block_below_stack = None
        for stack in stacks:
            for block in stack.get_blocks():
                if block.get_name() == block_name:
                    block_stack = stack
                elif block.get_name() == block_below_name:
                    block_below_stack = stack
        # if stacks are not equal, return invalid
        if block_stack != block_below_stack:
            action.set_invalid(f"Block {block_below_name} is not on the same stack as block {block_name}.")
            return False
        # return True in no invalidation reason could be found
        return True