from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import SimulationAction, UnstackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class BlockBelowRelationship(Constraint):
    """Constraint to check if one block is directly below another block."""

    def validate(self, state: SimulationState, action: UnstackAction) -> bool:
        block_name = action.get_block_name()
        block_below_name = action.get_block_below_name()
        stacks = state.get_stacks()
        for stack in stacks:
            blocks = stack.get_blocks()
            for i, block in enumerate(blocks):
                if block.get_name() == block_name:
                    if i == 0 or blocks[i-1].get_name() != block_below_name:
                        action.set_invalid(f"Block {block_below_name} is not below block {block_name}.")
                        return False
                    break
        # return True in no invalidation reason could be found
        return True