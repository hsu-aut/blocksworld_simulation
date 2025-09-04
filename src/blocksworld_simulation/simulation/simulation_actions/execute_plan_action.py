from blocksworld_simulation.api.request_models import ExecutePlanRequest
from blocksworld_simulation.simulation.simulation_actions import RobotAction
from blocksworld_simulation.simulation.simulation_actions import (
    PickUpAction,
    PutDownAction,
    StackAction,
    UnstackAction
)
from .simulation_action import SimulationAction
from ...api.request_models.execution_plan import (
    PickUpStep,
    PutDownStep,
    UnstackStep,
    StackStep
)
class ExecutePlanAction(SimulationAction):
    """Action for executing a simulation plan."""

    def __init__(self, request: ExecutePlanRequest):
        super().__init__()
        self._validation_mode = request.validation_mode
        self._steps = request.plan
        self._actions: list[RobotAction] = []
        for step in self._steps:
            if isinstance(step, PickUpStep):
                self._actions.append(PickUpAction(step))
            elif isinstance(step, PutDownStep):
                self._actions.append(PutDownAction(step))
            elif isinstance(step, StackStep):
                self._actions.append(StackAction(step))
            elif isinstance(step, UnstackStep):
                self._actions.append(UnstackAction(step))
        self._current_step_index: int = -1

    def is_in_validation_mode(self) -> bool:
        return self._validation_mode
    
    def get_actions(self) -> list[RobotAction]:
        return self._actions
    
    def increment_step(self):
        self._current_step_index += 1

    def reply_plan_invalid(self, invalid_step_message: str):
        # if counter has not been used, no steps were executed (this should not happen)
        if self._current_step_index == -1:
            return "Failed to execute plan, no steps were executed"
        # else report the executed steps and the first invalid step as well as the following steps that were not executed
        else:
            failure_message = "Failed to execute plan.\n"
            if self._current_step_index > 0:
                failure_message += f"Executed, valid steps:\n"
                for i in range(0, self._current_step_index):
                    failure_message += f" - Step {i + 1}: {self._steps[i]}\n"
            failure_message += "First invalid step:\n"
            failure_message += f" - Step {self._current_step_index + 1}: {self._steps[self._current_step_index]}\n"
            failure_message += f"   Reason: {invalid_step_message}\n"
            if self._current_step_index < len(self._steps) - 1:
                failure_message += "Following steps, that were not executed:\n"
                for i in range(self._current_step_index + 1, len(self._steps)):
                    failure_message += f" - Step {i + 1}: {self._steps[i]}\n"
        # return via reply queue
        self._is_valid = False
        self._reply_queue.put((False, failure_message))

    def _success_message(self):
        if self._validation_mode:
            return "Simulation plan is valid and can be executed."
        return "Simulation plan is valid and was executed successfully."

    def _failure_message(self) -> str:
        return "Failed to execute/validate plan"