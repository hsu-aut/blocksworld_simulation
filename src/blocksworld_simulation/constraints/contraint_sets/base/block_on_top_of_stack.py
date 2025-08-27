from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import SimulationAction, PickUpAction, StackAction, UnstackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class BlockOnTopOfStack(Constraint):
    """Constraint to check if a block is on top of its stack."""

    def validate(self, state: SimulationState, action: UnstackAction | StackAction | PickUpAction) -> bool:
        block_name = None
        if isinstance(action, (UnstackAction, PickUpAction)):
            block_name = action.get_block_name()
        elif isinstance(action, StackAction):
            block_name = action.get_target_block_name()
            # see if robot held block is the target block
            if block_name == state.get_robot().get_held_block().get_name():
                action.set_invalid(f"Block {block_name} is not on top of a stack.")
                return False          
        stacks = state.get_stacks()
        # find block in stacks
        for stack in stacks:
            for block in stack.get_blocks():
                if block.get_name() == block_name:
                    if stack.get_blocks()[-1].get_name() != block_name:
                        # if block is not on top of stack, return invalid
                        action.set_invalid(f"Block {block_name} is not on top of a stack.")
                        return False
                    # set the stack containing the block as the stack the block will be stacked on/unstacked from/picked up from
                    action.set_stack(stack)
                    break
        # return True in no invalidation reason could be found
        return True