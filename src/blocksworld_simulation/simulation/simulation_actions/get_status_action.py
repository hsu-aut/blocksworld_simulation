from queue import Queue
from .simulation_action import SimulationAction
from ...api.request_models import GetStatusRequest


class GetStatusAction(SimulationAction):
    """Action for getting the status of the simulation."""

    def __init__(self, reply_queue: Queue, request: GetStatusRequest):
        super().__init__(reply_queue)
        self._status_dict: dict = None

    def set_status_dict(self, status_dict: dict):
        self._status_dict = status_dict

    def _success_message(self):
        status_string = str(self._status_dict)
        return status_string

    def _failure_message(self) -> str:
        return "Simulation status could not be retrieved"