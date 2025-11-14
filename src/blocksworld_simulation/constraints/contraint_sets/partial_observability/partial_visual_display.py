from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class PartialVisualDisplay(Constraint):
    """Constraint to provide partial visibility of the simulation visual display.

    The top two blocks of each stack have their names displayed. All other blocks
    in a stack are shown but without their names. This matches the partial
    observability constraint where only the top two blocks can be identified
    with the status tool.
    """

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        # Update which block names are hidden for all stacks whenever this constraint is checked
        # This applies regardless of whether the simulation is running, as it's only for visualization
        self._update_hidden_names(state)
        # return True (this constraint only updates visibility, does not invalidate actions)
        return True

    def _update_hidden_names(self, state: SimulationState) -> None:
        """Update which blocks have their names hidden from visualization.

        Only the top two blocks (last two blocks) of each stack display their names.
        All other blocks are shown but without names.
        """
        for stack in state.get_stacks():
            blocks = stack.get_blocks()

            # Hide names for all blocks except the top 2
            for position, block in enumerate(blocks):
                if position < len(blocks) - 2:
                    # Hide name for blocks deeper than position 2
                    block.set_hide_name(True)
                else:
                    # Show name for top 2 blocks
                    block.set_hide_name(False)
