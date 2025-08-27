from typing import List
from blocksworld_simulation.simulation.robot import Robot
from blocksworld_simulation.simulation.stack import Stack
from blocksworld_simulation.simulation.block import Block


class SimulationState:
    """Class to represent the state of the simulation."""

    def __init__(self, simulation_running: bool = False, robot: Robot = None, stacks: List[Stack] = None):
        self._simulation_running: bool = simulation_running
        self._robot: Robot = robot
        self._stacks: List[Stack] = stacks
    
    def get_simulation_running(self) -> bool:
        """Get whether the simulation is running."""
        return self._simulation_running
    
    def set_simulation_running(self, running: bool):
        """Set whether the simulation is running."""
        self._simulation_running = running

    def get_robot(self) -> Robot:
        """Get the robot."""
        return self._robot
    
    def set_robot(self, robot: Robot):
        """Set the robot."""
        self._robot = robot
    
    def get_stacks(self) -> List[Stack]:
        """Get the list of stacks."""
        return self._stacks
    
    def set_stacks(self, stacks: List[Stack]):
        """Set the list of stacks."""
        self._stacks = stacks
    
    def get_robot_held_block(self) -> Block:
        """Get the block currently held by the robot."""
        return self._robot.get_held_block() if self._robot is not None else None
    
    def get_all_blocks(self) -> List[Block]:
        """Get all blocks in the simulation (from stacks and robot)."""
        all_blocks: List[Block] = [block for stack in self._stacks for block in stack.get_blocks()] if self._stacks else []
        if self.get_robot_held_block() is not None:
            all_blocks.append(self.get_robot_held_block())
        return all_blocks

    def to_dict(self) -> dict:
        """Convert simulation state to dictionary format."""
        return {
            "stacks": [stack.to_dict() for stack in self._stacks],
            "robot": self._robot.to_dict()
        }