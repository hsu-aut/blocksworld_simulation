from .simulation_action import SimulationAction


class GetFullStatusAction(SimulationAction):
    """Action for getting the full status of the simulation.

    Unlike GetStatusAction, this always returns all blocks with their names,
    even when partial observability constraints are active.
    """

    def __init__(self):
        super().__init__()
        self._status_dict: dict = None

    def set_status_dict(self, status_dict: dict):
        self._status_dict = status_dict

    def _success_message(self):
        status_string = str(self._status_dict)
        return status_string

    def _failure_message(self) -> str:
        return "Full simulation status could not be retrieved"
