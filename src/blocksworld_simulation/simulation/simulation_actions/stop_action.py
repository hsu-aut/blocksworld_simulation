from queue import Queue
from .simulation_action import SimulationAction
from ...api.request_models import StopSimulationRequest


class StopAction(SimulationAction):
    """Action for stopping the simulation."""

    def __init__(self, reply_queue: Queue, _request: StopSimulationRequest):
        super().__init__(reply_queue)

    def _success_message(self):
        return "Simulation stopped"

    def _failure_message(self) -> str:
        return "Simulation could not be stopped"