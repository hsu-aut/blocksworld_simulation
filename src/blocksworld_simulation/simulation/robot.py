import logging
from enum import Enum

import pygame

from .simulation_actions import RobotAction, PickUpAction, PutDownAction, StackAction, UnstackAction
from .block import Block

logger = logging.getLogger(__name__)

# Constants for robot 
SPEED = 10
""" speed of the robot movement (vertical and horizontal) """
TOP_GRIP_HEIGHT = 100
""" the uppermost robot y position """
# Constants for visual appearance
ROBOT_COLORS = [(150, 150, 150), (200, 200, 200)]
ROBOT_BORDER_RADIUS = 8
ROBOT_BASE_WIDTH = 100
ROBOT_BASE_HEIGHT = 30
ROBOT_ARM_WIDTH = 20
ROBOT_GRIP_WIDTH = 100
ROBOT_GRIP_HEIGHT = 20
ROBOT_FINGER_WIDTH = 10
ROBOT_FINGER_HEIGHT = ROBOT_GRIP_HEIGHT + 20

# define robot states as enum
class RobotState(Enum):
        IDLE = "idle"
        MOVING_TO_PICK = "moving_to_pick"
        PICKING = "picking"
        LIFTING = "lifting"
        HOLDING = "holding"
        MOVING_TO_PLACE = "moving_to_place"
        LOWERING = "lowering"
        RELEASING = "releasing"

class Robot:
    """Represents the robot arm that can manipulate blocks.
    Handles a "state machine", the moving logic and the visual apperance of the robot."""

    def __init__(self):
        self._x = 500
        self._y = TOP_GRIP_HEIGHT
        self._target_x = 700
        self._target_y = 300
        self._state = RobotState.IDLE
        self._validation_mode = False
        self._held_block: Block = None
        self._action_in_progress: RobotAction = None

    def get_state(self) -> RobotState:
        """Get the current state of the robot"""
        return self._state
    
    def get_held_block(self) -> Block:
        """Get the block currently held by the robot, if any"""
        return self._held_block
    
    def is_available(self) -> bool:
        """Check if the robot is available for a new action"""
        return (self._state == RobotState.IDLE or self._state == RobotState.HOLDING) and self._action_in_progress is None

    def set_validation_mode(self, validation_mode: bool):
        """Set the robot to validation mode mode, in which actions are executed instantly, without visual feedback."""
        self._validation_mode = validation_mode

    def set_action(self, action: RobotAction):
        """Set a new action for the robot to execute"""
        self._action_in_progress = action

    def to_dict(self) -> dict:
        """Convert the robot to a dictionary representation"""
        out_dict: dict = {
            "state": self._state.value,
            "held_block": self._held_block.to_dict() if self._held_block is not None else None
        }
        return out_dict

    def update_state(self):
        """Update the robot's state"""
        # if robot is idle, check for new pick up and put down commands
        if self._state == RobotState.IDLE:
            if self._action_in_progress is None:
                return
            elif isinstance(self._action_in_progress, PickUpAction) or isinstance(self._action_in_progress, UnstackAction):
                self._target_x = self._action_in_progress.get_target()[0]
                self._target_y = self._action_in_progress.get_target()[1]
                self._state = RobotState.MOVING_TO_PICK
                return
            return
        # if robot is holding a block, check for put down (or stack) commands
        if self._state == RobotState.HOLDING:
            if self._action_in_progress is None:
                return
            elif isinstance(self._action_in_progress, PutDownAction) or isinstance(self._action_in_progress, StackAction):
                self._target_x = self._action_in_progress.get_target()[0]
                self._target_y = self._action_in_progress.get_target()[1]
                self._state = RobotState.MOVING_TO_PLACE
                return
            return
        # if moving to pick up a block, move until target x is reached, then transition to picking
        if self._state == RobotState.MOVING_TO_PICK:
            if abs(self._x - self._target_x) > SPEED and not self._validation_mode:
                self._x += SPEED if self._x < self._target_x else -SPEED
            else:
                self._x = self._target_x
                self._state = RobotState.PICKING
            return
        # if picking, move until target y is reached, then transition to LIFTING
        if self._state == RobotState.PICKING and isinstance(self._action_in_progress, (UnstackAction, PickUpAction)):
            if abs(self._y - self._target_y) > SPEED and not self._validation_mode:
                self._y += SPEED 
            else:
                self._y = self._target_y
                self._held_block = self._action_in_progress.get_block()
                self._action_in_progress.get_stack().remove_top_block()
                self._state = RobotState.LIFTING
            return
        # if lifting, move until top grip height is reached, then transition to HOLDING
        if self._state == RobotState.LIFTING:
            if abs(self._y - TOP_GRIP_HEIGHT) > SPEED and not self._validation_mode:
                self._y -= SPEED
                self._held_block.set_position_on_robot(self._x, self._y)
            else:
                self._y = TOP_GRIP_HEIGHT
                self._held_block.set_position_on_robot(self._x, self._y)
                # send success feedback and clear the action
                self._action_in_progress.reply_success()
                self._action_in_progress = None
                self._state = RobotState.HOLDING
            return
        # if robot is moving to place a block, move until target x is reached, then transition to LOWERING
        if self._state == RobotState.MOVING_TO_PLACE:
            if abs(self._x - self._target_x) > SPEED and not self._validation_mode:
                self._x += SPEED if self._x < self._target_x else -SPEED
                self._held_block.set_position_on_robot(self._x, self._y)
            else:
                self._x = self._target_x
                self._held_block.set_position_on_robot(self._x, self._y)
                self._state = RobotState.LOWERING
            return
        # if robot is lowering, move until target y is reached, then transition to RELEASING
        if self._state == RobotState.LOWERING and isinstance(self._action_in_progress, (StackAction, PutDownAction)):
            if abs(self._y - self._target_y) > SPEED and not self._validation_mode:
                self._y += SPEED
                self._held_block.set_position_on_robot(self._x, self._y)
            else:
                self._y = self._target_y
                self._held_block.set_position_on_robot(self._x, self._y)
                self._action_in_progress.get_stack().add_block(self._held_block)
                self._held_block = None
                self._state = RobotState.RELEASING
            return
        # if robot is releasing, move until top grip height is reached, then transition to IDLE
        if self._state == RobotState.RELEASING:
            if abs(self._y - TOP_GRIP_HEIGHT) > SPEED and not self._validation_mode:
                self._y -= SPEED
            else:
                self._y = TOP_GRIP_HEIGHT
                self._state = RobotState.IDLE
                # send success feedback and clear the action
                self._action_in_progress.reply_success()
                self._action_in_progress = None
            return

    def draw(self, surface):
        """Draw the robot on the given surface"""
        # Draw the robot base
        base_rect = pygame.Rect(self._x - ROBOT_BASE_WIDTH // 2, 0, ROBOT_BASE_WIDTH, ROBOT_BASE_HEIGHT)
        pygame.draw.rect(
            surface, ROBOT_COLORS[0], base_rect, 
            border_bottom_left_radius=ROBOT_BORDER_RADIUS, border_bottom_right_radius=ROBOT_BORDER_RADIUS)
        # Draw the robot arm
        arm_rect = pygame.Rect(
            self._x - ROBOT_ARM_WIDTH // 2, ROBOT_BASE_HEIGHT, 
            ROBOT_ARM_WIDTH, self._y - ROBOT_GRIP_HEIGHT - ROBOT_BASE_HEIGHT
        )
        pygame.draw.rect(surface, ROBOT_COLORS[1], arm_rect)
        # Draw the robot grip
        grip_rect = pygame.Rect(
            self._x - ROBOT_GRIP_WIDTH // 2, self._y - ROBOT_GRIP_HEIGHT, 
            ROBOT_GRIP_WIDTH, ROBOT_GRIP_HEIGHT
        )
        pygame.draw.rect(
            surface, ROBOT_COLORS[0], grip_rect,
            border_top_left_radius=ROBOT_BORDER_RADIUS, border_top_right_radius=ROBOT_BORDER_RADIUS
        )
        # draw held block (if any)
        if self._held_block is not None:
            self._held_block.draw(surface)
        return