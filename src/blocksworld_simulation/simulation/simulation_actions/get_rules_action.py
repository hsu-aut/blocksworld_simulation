from .simulation_action import SimulationAction


class GetRulesAction(SimulationAction):
    """Action for getting simulation rules."""

    def __init__(self):
        super().__init__()
        self._rules: str = None

    def set_rules(self, rules: str):
        self._rules = rules

    def _success_message(self):
        return self._rules

    def _failure_message(self) -> str:
        return "Could not retrieve simulation rules"