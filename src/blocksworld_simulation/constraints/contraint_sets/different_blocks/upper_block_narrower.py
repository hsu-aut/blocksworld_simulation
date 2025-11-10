from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import StackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class UpperBlockNarrower(Constraint):
    """Constraint to check if a block is stacked on a wider block."""

    def validate(self, state: SimulationState, action: StackAction) -> Tuple[bool, str]:
        block_width = action.get_block().get_size()[0]
        target_block_width = action.get_target_block().get_size()[0]
        # Check if the block is stacked on a wider block
        if target_block_width < block_width:
            action.set_invalid("Block cannot be stacked on a smaller block.")
            return False
        # return True in no invalidation reason could be found
        return True