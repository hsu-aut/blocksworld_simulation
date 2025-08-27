from queue import Queue
from abc import ABC, abstractmethod


class SimulationAction(ABC):
    """Base class for actions in the simulation.
    Actions can be created by user input or by the API.
    They are created in an unvalidated state and then validated by the constraint manager."""

    def __init__(self):
        self._reply_queue: Queue = None
        self._is_valid: bool | None = None

    def set_reply_queue(self, reply_queue: Queue):
        self._reply_queue = reply_queue

    def is_valid(self) -> bool | None:
        """Check if the action has been validated. Returns True if valid, False if invalid, None if not yet validated."""
        return self._is_valid
    
    def set_valid(self):
        """Mark the action as validated"""
        self._is_valid = True

    def set_invalid(self, invalid_reason: str):
        """Mark the action as invalidated"""
        self._is_valid = False
        self._reply_queue.put((False, self._failure_message() + " - " + invalid_reason))

    def reply_success(self):
        """Send a success reply back to the reply queue"""
        self._reply_queue.put((True, self._success_message()))

    @abstractmethod
    def _success_message(self) -> str:
        """Defines the success message to be sent back to the reply queue if action was successfully executed.
        Must be implemented by subclasses to send a success reply"""
        pass

    @abstractmethod
    def _failure_message(self) -> str:
        """Defines the failure message to be sent back to the reply queue if action was not successfully executed.
        Must be implemented by subclasses to send a failure reply"""
        pass