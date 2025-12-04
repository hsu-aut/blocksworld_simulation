from blocksworld_simulation.constraints.constraint_set import ConstraintSet
from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.partial_observability.partial_observability import PartialObservabilityConstraintSet
from blocksworld_simulation.constraints.contraint_sets.block_size.block_size import BlockSizeConstraintSet
from blocksworld_simulation.simulation.simulation_actions import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class ConstraintManager:
    def __init__(self):
        self._active_constraint_set: ConstraintSet = BaseConstraintSet()
        self._constraint_sets: dict[str, ConstraintSet] = {
            "base": BaseConstraintSet(),
            "block_size": BlockSizeConstraintSet(),
            "partial_observability": PartialObservabilityConstraintSet()
            
        }

    def _find_set_by_name(self, name: str) -> ConstraintSet | None:
        """Get a constraint set instance by name."""
        constraint_set: ConstraintSet | None = self._constraint_sets.get(name)
        if constraint_set:
            return constraint_set
        return None

    def constraint_set_exists(self, name: str) -> bool:
        """Check if a constraint set exists by name."""
        return name in self._constraint_sets

    def set_constraint_set(self, name: str):
        """Set the active constraint set by name."""
        constraint_set = self._find_set_by_name(name)
        self._active_constraint_set = constraint_set

    def get_constraint_set(self) -> ConstraintSet:
        """Get the active constraint set."""
        return self._active_constraint_set

    def get_rules(self) -> str:
        """Get the rules from the active constraint set."""
        return self._active_constraint_set.get_rules()

    def validate_action(self, action: SimulationAction, state: SimulationState):
        """Validate an action against the active constraint set."""
        return self._active_constraint_set.validate(state, action)

constraint_manager = ConstraintManager()