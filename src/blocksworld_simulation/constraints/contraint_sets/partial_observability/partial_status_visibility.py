from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import GetStatusAction, GetFullStatusAction, SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class PartialStatusVisibility(Constraint):
    """Constraint to provide partial visibility of the simulation status.

    The top two blocks of each stack are fully identified. All other blocks
    in a stack are marked as "unknown". This allows for unstack operations
    while maintaining uncertainty about deeper blocks.
    """

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        if not state.get_simulation_running():
            action.set_invalid("Simulation is not running.")
            return False
        # if the action is a GetStatusAction (but not GetFullStatusAction), set the partial status info
        if isinstance(action, GetStatusAction) and not isinstance(action, GetFullStatusAction):
            action.set_status_dict(self._create_partial_status(state))
        # return True if no invalidation reason could be found
        return True

    def _create_partial_status(self, state: SimulationState) -> dict:
        """Create a status dict where only the top two blocks are fully visible.

        The status shows:
        - All blocks in each stack with their properties (size, weight, type)
        - Top two blocks (last two blocks) with full identity and details (name, size, etc.)
        - Hidden blocks (deeper than 2 positions) with name replaced by "unknown"
        - Robot state and held block (if any)

        This ensures unstack operations are possible (you know which block is on top
        and which block is below it) while maintaining uncertainty about deeper blocks.
        """
        partial_stacks = []

        for stack in state.get_stacks():
            blocks = stack.get_blocks()
            stack_dict = {
                "number": stack.get_number(),
                "blocks": []
            }

            # Add all blocks, but only the top block is fully visible
            for position, block in enumerate(blocks):
                block_dict = block.to_dict()
                block_dict["position"] = position

                # For hidden blocks (not the top block), replace name with "unknown"
                if position < len(blocks) - 2:  # Not the top block
                    block_dict["name"] = "unknown"

                stack_dict["blocks"].append(block_dict)

            partial_stacks.append(stack_dict)

        return {
            "stacks": partial_stacks,
            "robot": state.get_robot().to_dict()
        }
