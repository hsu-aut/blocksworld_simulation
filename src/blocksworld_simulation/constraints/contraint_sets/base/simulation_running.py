from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import GetStatusAction, SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class SimulationRunning(Constraint):
    """Constraint to check if the simulation is currently running."""

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        if not state.get_simulation_running():
            action.set_invalid("Simulation is not running.")
            return False
        # if the action is a GetStatusAction, set the status info
        if isinstance(action, GetStatusAction):
            action.set_status_dict(state.to_dict())
        # return True in no invalidation reason could be found
        return True