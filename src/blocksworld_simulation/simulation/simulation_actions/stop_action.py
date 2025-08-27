from .simulation_action import SimulationAction


class StopAction(SimulationAction):
    """Action for stopping the simulation."""

    def __init__(self):
        super().__init__()

    def _success_message(self):
        return "Simulation stopped"

    def _failure_message(self) -> str:
        return "Simulation could not be stopped"