from .simulation_action import SimulationAction


class GetStatusAction(SimulationAction):
    """Action for getting the status of the simulation."""

    def __init__(self):
        super().__init__()
        self._status_dict: dict = None

    def set_status_dict(self, status_dict: dict):
        self._status_dict = status_dict

    def _success_message(self):
        status_string = str(self._status_dict)
        return status_string

    def _failure_message(self) -> str:
        return "Simulation status could not be retrieved"