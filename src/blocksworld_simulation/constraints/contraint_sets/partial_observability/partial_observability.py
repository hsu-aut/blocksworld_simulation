from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_observability_rules import get_partial_observability_rules
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_status_visibility import PartialStatusVisibility
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_visual_display import PartialVisualDisplay


class PartialObservabilityConstraintSet(BaseConstraintSet):
    """Constraint set for the partial observability extension"""

    def __init__(self):
        super().__init__()

        # Create a single instance of PartialVisualDisplay to update hidden blocks
        partial_visual_display = PartialVisualDisplay()

        # GET STATUS: PartialStatusVisibility (instead of SimulationRunning)
        # This replaces the normal SimulationRunning constraint with PartialStatusVisibility
        self._get_status_constraints.extend([
            PartialStatusVisibility()
        ])

        # VISUAL DISPLAY: Add PartialVisualDisplay to action-specific constraint lists
        # This updates the hidden blocks for each stack during action validation
        self._pick_up_constraints.extend([partial_visual_display])
        self._put_down_constraints.extend([partial_visual_display])
        self._stack_constraints.extend([partial_visual_display])
        self._unstack_constraints.extend([partial_visual_display])
        self._get_status_constraints.extend([partial_visual_display])
        self._plan_constraints.extend([partial_visual_display])

        # Rules: first explain the base blocksworld rules and then add the partial observability rules
        self._rules = self._rules + get_partial_observability_rules() 

