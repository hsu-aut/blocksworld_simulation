from queue import Queue
from .simulation_action import SimulationAction
from ...api.request_models import GetRulesRequest


class GetRulesAction(SimulationAction):
    """Action for getting simulation rules."""

    def __init__(self, reply_queue: Queue, request: GetRulesRequest):
        super().__init__(reply_queue)
        self._rules: str = None

    def set_rules(self, rules: str):
        self._rules = rules

    def _success_message(self):
        return self._rules

    def _failure_message(self) -> str:
        return "Could not retrieve simulation rules"