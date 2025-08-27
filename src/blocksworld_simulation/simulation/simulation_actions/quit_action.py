from queue import Queue
from .simulation_action import SimulationAction


class QuitAction(SimulationAction):
    """Action for quitting the application."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)

    def _success_message(self):
        return "Application is quitting"

    def _failure_message(self) -> str:
        return "Application could not be quit"