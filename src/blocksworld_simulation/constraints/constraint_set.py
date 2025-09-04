from abc import ABC
from typing import List
from blocksworld_simulation.simulation.simulation_state import SimulationState

from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import (
    GetRulesAction, PreStartAction, SimulationAction, 
    StartAction, StopAction, QuitAction, PickUpAction, 
    PutDownAction, StackAction, UnstackAction, ExecutePlanAction,
    GetStatusAction, GetScenarioAction
)


class ConstraintSet(ABC):
    """Abstract base class for all constraint sets."""
    
    def __init__(self):
        # the constructor defines these fields, they have to be extended by implementing classes
        self._quit_constraints: List[Constraint] = []
        self._pre_start_constraints: List[Constraint] = []
        self._start_constraints: List[Constraint] = []
        self._stop_constraints: List[Constraint] = []
        self._get_status_constraints: List[Constraint] = []
        self._pick_up_constraints: List[Constraint] = []
        self._put_down_constraints: List[Constraint] = []
        self._stack_constraints: List[Constraint] = []
        self._unstack_constraints: List[Constraint] = []
        self._execute_plan_constraints: List[Constraint] = []
        self._get_rules_constraints: List[Constraint] = []
        self._get_scenario_constraints: List[Constraint] = []
        self._rules: str = ""

    def _get_constraints_for_action(self, action: SimulationAction) -> List[Constraint]:
        """Get the appropriate constraint list based on action type."""
        if isinstance(action, QuitAction):
            return self._quit_constraints
        elif isinstance(action, PreStartAction):
            return self._pre_start_constraints
        elif isinstance(action, StartAction):
            return self._start_constraints
        elif isinstance(action, StopAction):
            return self._stop_constraints
        elif isinstance(action, GetStatusAction):
            return self._get_status_constraints
        elif isinstance(action, GetRulesAction):
            return self._get_rules_constraints
        elif isinstance(action, GetScenarioAction):
            return self._get_scenario_constraints
        elif isinstance(action, PickUpAction):
            return self._pick_up_constraints
        elif isinstance(action, PutDownAction):
            return self._put_down_constraints
        elif isinstance(action, StackAction):
            return self._stack_constraints
        elif isinstance(action, UnstackAction):
            return self._unstack_constraints
        elif isinstance(action, ExecutePlanAction):
            return self._execute_plan_constraints
        else:
            return []

    def validate(self, state: SimulationState, action: SimulationAction):
        """Validate action against appropriate constraint set based on action type."""
        constraint_list = self._get_constraints_for_action(action)
        for constraint in constraint_list:
            is_valid = constraint.validate(state, action)
            # if any constraint is not satisfied, just return, the action set invalid by the constraint
            if not is_valid:
                return
        # if all constraints are satisfied, validate the action and return
        action.set_valid()
        return

    def get_rules(self) -> str:
        """Get the rules from the active constraint set."""
        return self._rules