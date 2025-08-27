from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class SimulationNotRunning(Constraint):
    """Constraint to check if the simulation is currently not running."""

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        if state.get_simulation_running():
            action.set_invalid("Simulation is already running.")
            return False
        # return True in no invalidation reason could be found
        return True