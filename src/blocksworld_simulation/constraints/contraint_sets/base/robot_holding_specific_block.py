from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import SimulationAction, PutDownAction, StackAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class RobotHoldingSpecificBlock(Constraint):
    """Constraint to check if the robot is holding a specific block."""

    def validate(self, state: SimulationState, action: PutDownAction | StackAction) -> bool:
        block_name = action.get_block_name()
        robot_held_block = state.get_robot_held_block()
        # check if the robot is holding the correct block
        if robot_held_block is None or robot_held_block.get_name() != block_name:
            action.set_invalid(f"Robot is not holding block {block_name}.")
            return False
        # return True in no invalidation reason could be found
        return True