from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.block import Block
from blocksworld_simulation.simulation.simulation_action import SimulationAction, PickUpAction, PutDownAction, StackAction, UnstackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class BlockExists(Constraint):
    """Constraint to check if a block exists in the simulation."""

    def validate(self, state: SimulationState, action: PickUpAction | PutDownAction | StackAction | UnstackAction) -> bool:
        blocks = state.get_all_blocks()
        # find first block (all robot actions)
        block_1_name = action.get_block_name()
        block_1: Block = None
        for block in blocks:
            if block.get_name() == block_1_name:
                block_1 = block
                break
        # if block 1 is not found, return invalid
        if block_1 is None:
            action.set_invalid(f"Block {block_1_name} does not exist in the simulation.")
            return False
        # set the found block as the block to be picked up/put down/stacked/unstacked
        action.set_block(block_1)
        # find the block the first block will be stacked on (only for stack)
        if isinstance(action, StackAction):
            block_2_name = action.get_target_block_name()
            block_2: Block = None
            for block in blocks:
                if block.get_name() == block_2_name:
                    block_2 = block
                    break
            # if block 2 is not found, return invalid
            if block_2 is None:
                action.set_invalid(f"Block {block_2_name} does not exist in the simulation.")
                return False
            # set the found block as the target the first block will be stacked on
            action.set_target_block(block_2)
        # find the block the first block will be unstacked from (only for unstack)
        elif isinstance(action, UnstackAction):
            block_2_name = action.get_block_below_name()
            for block in blocks:
                if block.get_name() == block_2_name:
                    block_2 = block
                    break
            # if block 2 is not found, return invalid
            if block_2 is None:
                action.set_invalid(f"Block {block_2_name} does not exist in the simulation.")
                return False
            # set the found block as the block below the first block
            action.set_block_below(block_2)
        # return True in no invalidation reason could be found
        return True