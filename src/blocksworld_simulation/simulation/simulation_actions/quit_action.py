from .simulation_action import SimulationAction


class QuitAction(SimulationAction):
    """Action for quitting the application."""

    def __init__(self):
        super().__init__()

    def _success_message(self):
        return "Application is quitting"

    def _failure_message(self) -> str:
        return "Application could not be quit"