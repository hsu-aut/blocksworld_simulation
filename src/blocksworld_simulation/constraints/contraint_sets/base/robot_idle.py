from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState
from blocksworld_simulation.simulation.robot import RobotState


class RobotIdle(Constraint):
    """Constraint to check if the robot is currently idle."""

    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        robot = state.get_robot()
        if robot is None or robot.get_state() != RobotState.IDLE:
            action.set_invalid("Robot is not idle.")
            return False
        # return True in no invalidation reason could be found
        return True