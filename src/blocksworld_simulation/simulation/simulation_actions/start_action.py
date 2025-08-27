from queue import Queue
from .simulation_action import SimulationAction


class StartAction(SimulationAction):
    """Action for starting the simulation."""

    def __init__(self, reply_queue: Queue, stack_config=None, scenario_id=None, constraint_set=None):
        super().__init__(reply_queue)
        self._stack_config = stack_config
        self._scenario_id = scenario_id
        self._constraint_set = constraint_set

    def get_stack_config(self):
        """Get the stack configuration for the simulation"""
        return self._stack_config
    
    def get_scenario_id(self):
        """Get the scenario ID for the simulation"""
        return self._scenario_id
    
    def get_constraint_set(self):
        """Get the constraint set name for the simulation"""
        return self._constraint_set
    
    def _success_message(self):
        config_str = f"given stack config: {self._stack_config}" if self._stack_config is not None else "random stacks"
        return f"Simulation started with {config_str}"

    def _failure_message(self) -> str:
        return "Simulation could not be started"