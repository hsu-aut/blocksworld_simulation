from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_observability_rules import get_partial_observability_rules
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_status_visibility import PartialStatusVisibility


class PartialObservabilityConstraintSet(BaseConstraintSet):
    """Constraint set for the partial observability extension"""

    def __init__(self):
        super().__init__()

        # GET STATUS: PartialStatusVisibility (instead of SimulationRunning)
        # This replaces the normal SimulationRunning constraint with PartialStatusVisibility
        self._get_status_constraints.extend([
            PartialStatusVisibility()
        ])

        # Rules: first explain the base blocksworld rules and then add the partial observability rules
        self._rules = self._rules + get_partial_observability_rules() 

