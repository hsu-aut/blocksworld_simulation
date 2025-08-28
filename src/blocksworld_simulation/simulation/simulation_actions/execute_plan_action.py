from typing import Union
from blocksworld_simulation.api.request_models import ExecutePlanRequest
from .simulation_action import SimulationAction
from ...api.request_models import (
    PickUpRequest,
    PutDownRequest,
    StackRequest,
    UnstackRequest
)

class ExecutePlanAction(SimulationAction):
    """Action for executing a simulation plan."""

    def __init__(self, request: ExecutePlanRequest):
        super().__init__()
        self._validation = request.validation
        self._steps = request.plan
        self._first_invalid_step_index: int = None
        self._first_invalid_step: Union[ PickUpRequest, PutDownRequest, StackRequest, UnstackRequest] = None

    def set_first_invalid_step(self, index: int):
        self._first_invalid_step_index = index
        self._first_invalid_step = self._steps[index]

    def _success_message(self):
        if self._validation:
            return "Simulation plan is valid and can be executed."
        return "Simulation plan is valid and was executed successfully."

    def _failure_message(self) -> str:
        if self._first_invalid_step_index is not None:
            return f"Simulation plan is invalid. First invalid step at index [{self._first_invalid_step_index}]: {self._steps[self._first_invalid_step_index]}"
        return "Failed to validate plan"