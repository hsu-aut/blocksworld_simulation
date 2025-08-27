from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import SimulationAction, PickUpAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class OnlyBlockInStack(Constraint):
    """Constraint to check if a block is alone on the ground (only block in its stack)."""

    def validate(self, state: SimulationState, action: PickUpAction) -> bool:
        block_name = action.get_block_name()
        stacks = state.get_stacks()
        # find block in stacks
        for stack in stacks:
            for block in stack.get_blocks():
                if block.get_name() == block_name:
                    if len(stack.get_blocks()) > 1:
                        action.set_invalid(f"Block {block_name} is not the only block in its stack.")
                        return False
                    break
        # return True in no invalidation reason could be found
        return True