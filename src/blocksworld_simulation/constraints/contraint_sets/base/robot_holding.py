from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState
from blocksworld_simulation.simulation.robot import RobotState


class RobotHolding(Constraint):
    """Constraint to check if the robot is currently holding a block."""

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        robot = state.get_robot()
        if robot is None or robot.get_state() != RobotState.HOLDING:
            action.set_invalid("Robot is not holding a block.")
            return False
        # return True in no invalidation reason could be found
        return True