from queue import Queue
from .simulation_action import SimulationAction
from ...api.request_models import GetScenarioRequest


class GetScenarioAction(SimulationAction):
    """Action for getting scenario information."""

    def __init__(self, reply_queue: Queue, request: GetScenarioRequest):
        super().__init__(reply_queue)
        self._scenario_name = request.scenario_name
        self._result_data = None

    def get_scenario_name(self) -> str:
        return self._scenario_name

    def set_result_data(self, result_data):
        self._result_data = result_data

    def _success_message(self):
        return self._result_data

    def _failure_message(self) -> str:
        return "Could not retrieve scenario information"