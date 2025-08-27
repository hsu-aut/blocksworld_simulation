from blocksworld_simulation.simulation.simulation_state import SimulationState
from blocksworld_simulation.simulation.simulation_action import SimulationAction
from blocksworld_simulation.constraints.constraint_set import ConstraintSet
from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet


class ConstraintManager:
    """Manager for validating simulation actions using configurable constraint sets."""
    
    def __init__(self, constraint_set: ConstraintSet = None):
        """Initialize the constraint manager with a specific constraint set."""
        self._constraint_set = constraint_set or BaseConstraintSet()
    
    def validate_action(self, simulation_action: SimulationAction, simulation_state: SimulationState):
        """Validate a simulation action against the currently active constraint set.
        This actually just passes the action to the currently active constraint set for validation."""
        self._constraint_set.validate(simulation_state, simulation_action)
        return
    
    def set_constraint_set(self, constraint_set: ConstraintSet):
        """Change the constraint set used for validation.
        """
        self._constraint_set = constraint_set