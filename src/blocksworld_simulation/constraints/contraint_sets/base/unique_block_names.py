
from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.simulation.simulation_action import StartAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class UniqueBlockNames(Constraint):
    """Constraint to check if all block names of a given stack configuration are unique."""

    def validate(self, state: SimulationState, action: StartAction) -> bool:
        stack_config = action.get_stack_config()
        # if stack_config is not None, check it 
        if stack_config is not None:
            block_names = []
            for stack in stack_config:
                for block in stack:
                    name = block if isinstance(block, str) else block.name
                    if name in block_names:
                        action.set_invalid(f'Block name "{name}" appears multiple times. Each block must have a unique name.')
                        return False
                    block_names.append(name)
        # If stack_config is None, it is valid, as random blocks will be assigned unique names.
        # also, if no invalid reasons were found, it is valid
        return True