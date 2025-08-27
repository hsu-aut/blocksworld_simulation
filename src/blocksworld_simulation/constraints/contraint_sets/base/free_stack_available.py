from typing import Tuple
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_actions import SimulationAction, PutDownAction
from blocksworld_simulation.simulation.simulation_state import SimulationState
from blocksworld_simulation.simulation.stack import Stack


class FreeStackAvailable(Constraint):
    """Constraint to check if there is at least one empty stack available."""

    def validate(self, state: SimulationState, action: PutDownAction) -> bool:
        stacks = state.get_stacks()
        # find a free stack to put down the block
        stack: Stack = None
        for _stack in stacks:
            if not _stack.get_blocks():
                stack = _stack
                break
        # if no free stack is found, return invalid
        if stack is None:
            action.set_invalid("No free stack is available.")
            return False
        # set the found free stack as the target stack
        action.set_stack(stack)
        # return True in no invalidation reason could be found
        return True