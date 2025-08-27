from typing import Tuple
from abc import abstractmethod
from .simulation_action import SimulationAction


class RobotAction(SimulationAction):
    """Base class for robot actions in the simulation."""

    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def get_target(self) -> Tuple[int, int]:
        """Get the target position for the action. Must be implemented by subclasses."""
        pass