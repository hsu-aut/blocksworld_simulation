from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import StartAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class ValidStartConfig(Constraint):
    """Constraint to validate Hanoi Towers start configuration."""

    def validate(self, state: SimulationState, action: StartAction) -> bool:
        stack_config = action.get_stack_config()
        # check minimum configuration - at least 2 stacks
        if len(stack_config) < 2:
            action.set_invalid("Hanoi Towers requires at least 2 stacks.")
            return False
        # Collect all blocks and their sizes, if x_size is not given, return invalid
        all_blocks = []
        block_sizes = []
        for stack in stack_config:
            for block in stack:
                all_blocks.append(block)
                x_size = getattr(block, 'x_size', None)
                if x_size is None:
                    action.set_invalid("Block missing x_size for Hanoi Towers.")
                    return False
                block_sizes.append(x_size)
        # if no blocks are present, return invalid
        if not all_blocks:
            action.set_invalid("Hanoi Towers requires at least one block.")
            return False
        # if block sizes are not unique, return invalid
        if len(block_sizes) != len(set(block_sizes)):
            action.set_invalid("Hanoi Towers requires all blocks to have unique x_size values.")
            return False
        # check structure - largest to smallest (bottom to top)
        for stack_index, stack in enumerate(stack_config):
            if len(stack) > 1:
                for i in range(len(stack) - 1):
                    bottom_block = stack[i]
                    top_block = stack[i + 1]
                    if bottom_block.x_size <= top_block.x_size:
                        action.set_invalid("Invalid Hanoi Tower structure. Wider blocks cannot be on top of narrower blocks.")
                        return False
        # return True in no invalidation reason could be found
        return True