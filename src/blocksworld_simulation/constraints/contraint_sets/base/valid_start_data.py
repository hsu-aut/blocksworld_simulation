from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.scenarios.scenario_manager import scenario_manager
from blocksworld_simulation.simulation.simulation_action import PreStartAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class ValidStartData(Constraint):
    """Constraint to check if the data to start the simulation is valid."""

    def validate(self, state: SimulationState, action: PreStartAction) -> bool:
        # get data from action
        constraint_set = action.get_constraint_set()
        scenario_id = action.get_scenario_id()
        stack_config = action.get_stack_config()
        # if constraint_set and scenario_id are not given, validate, and use base constraint set
        if constraint_set is None and scenario_id is None:
            action.set_constraint_set("base")
            return True
        # if too much parameters are given, invalidate
        elif scenario_id is not None and (stack_config is not None or constraint_set is not None):
            action.set_invalid("Cannot specify both scenario_id and stack_config/constraint_set")
            return False
        # if only scenario_id is given, check if it exists
        elif scenario_id is not None and constraint_set is None and stack_config is None:
            scenario = scenario_manager.get_scenario(scenario_id) or None
            if scenario is not None:
                constraint_set = scenario.constraint_set or None
                stack_config = scenario.initial_state.stacks or None
                if constraint_set is not None:
                    from blocksworld_simulation.constraints.constraint_manager import constraint_manager # Import locally to avoid circular dependency
                    if constraint_manager.constraint_set_exists(constraint_set):
                        action.set_constraint_set(constraint_set)
                        if stack_config is not None:
                            action.set_stack_config(stack_config)
                            return True
                        action.set_invalid("No stack configuration in scenario")
                        return False
                action.set_invalid("Unknown constraint set in scenario")
                return False
            action.set_invalid("Unknown scenario ID")
            return False
        # if only constraint set is given, only pass if its base, as there are no random initializations for other constraint sets
        elif constraint_set is not None and stack_config is None and scenario_id is None:
            if constraint_set == "base":
                return True
            action.set_invalid("If constraint set is specified without stack_config, it must be 'base'")
            return False
        # if stack_config and constraint_set are given, pass, the validity of the stack_config is checked later
        elif stack_config is not None and constraint_set is not None and scenario_id is None:
            # however, check if constraint set exists
            from blocksworld_simulation.constraints.constraint_manager import constraint_manager
            if constraint_manager.constraint_set_exists(constraint_set):
                return True
            action.set_invalid("Unknown constraint set")
            return False
        # error case, should not reach here
        else:
            action.set_invalid("Unknown constraint set validation error")
            return False