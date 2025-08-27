from typing import Optional
from .simulation_action import SimulationAction


class GetScenarioAction(SimulationAction):
    """Action for getting scenario information."""

    def __init__(self, scenario_name: Optional[str] = None):
        super().__init__()
        self._scenario_name = scenario_name
        self._result_data = None

    def get_scenario_name(self) -> str:
        return self._scenario_name

    def set_result_data(self, result_data):
        self._result_data = result_data

    def _success_message(self):
        return self._result_data

    def _failure_message(self) -> str:
        return "Could not retrieve scenario information"