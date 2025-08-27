from .simulation_action import SimulationAction
from .start_action import StartAction
from ...api.request_models import StartSimulationRequest


class PreStartAction(SimulationAction):
    """Action for changing the constraint set before starting the simulation with a StartAction."""

    def __init__(self, request: StartSimulationRequest):
        super().__init__()
        self._stack_config = request.initial_stacks
        self._scenario_id = request.scenario_id
        self._constraint_set = request.constraint_set
    
    def get_constraint_set(self) -> str | None:
        """Get the new constraint set to be applied."""
        return self._constraint_set

    def set_constraint_set(self, constraint_set: str):
        """Set the new constraint set to be applied."""
        self._constraint_set = constraint_set

    def get_scenario_id(self) -> str | None:
        """Get the scenario ID for the simulation"""
        return self._scenario_id
    
    def get_stack_config(self):
        """Get the initial stacks for the simulation"""
        return self._stack_config
    
    def set_stack_config(self, stack_config):
        """Set the initial stacks for the simulation"""
        self._stack_config = stack_config

    def create_start_action(self) -> StartAction:
        """Create a StartAction with the current parameters."""
        start_action = StartAction(
            stack_config=self._stack_config,
            scenario_id=self._scenario_id,
            constraint_set=self._constraint_set
        )
        start_action.set_reply_queue(self._reply_queue)
        return start_action

    def _success_message(self):
        return f"Constraint set changed to {self._constraint_set}"

    def _failure_message(self) -> str:
        return "Constraint set could not be changed"