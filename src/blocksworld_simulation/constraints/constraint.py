from abc import ABC, abstractmethod

from blocksworld_simulation.simulation.simulation_actions import SimulationAction
from blocksworld_simulation.simulation.simulation_state import SimulationState
    

class Constraint(ABC):
    """Abstract base class for all constraints."""

    @abstractmethod
    def validate(self, state: SimulationState, action: SimulationAction) -> bool:
        """Validate the action against the current simulation state.
        Returns: True if the action is valid and False - if the action is invalid.
        The reason for failure has to be set in the action object.
        """
        pass