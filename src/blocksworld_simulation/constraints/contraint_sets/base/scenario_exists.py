from blocksworld_simulation.constraints.constraint import Constraint
from blocksworld_simulation.scenarios.scenario_manager import scenario_manager
from blocksworld_simulation.simulation.simulation_actions.get_scenarios_action import GetScenarioAction
from blocksworld_simulation.simulation.simulation_state import SimulationState


class ScenarioExists(Constraint):
    """Constraint to check if the scenario exists."""

    def validate(self, state: SimulationState, action: GetScenarioAction) -> bool:
        # get data from action
        scenario_name_or_id = action.get_scenario_name()
        # if None, all scenarios are returned
        if scenario_name_or_id is None:
            return True
        # else, check if scenario exists
        else:
            if scenario_manager.scenario_exists(scenario_name_or_id):
                return True
            action.set_invalid("Unknown scenario")
            return False
       