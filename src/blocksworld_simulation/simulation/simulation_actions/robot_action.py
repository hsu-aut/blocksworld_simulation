from typing import Tuple
from queue import Queue
from abc import abstractmethod
from .simulation_action import SimulationAction


class RobotAction(SimulationAction):
    """Base class for robot actions in the simulation."""

    def __init__(self, reply_queue: Queue):
        super().__init__(reply_queue)
    
    @abstractmethod
    def get_target(self) -> Tuple[int, int]:
        """Get the target position for the action. Must be implemented by subclasses."""
        pass