from typing import Optional, Tuple
import pygame
import random
from pydantic import BaseModel, Field
import re

DEFAULT_BLOCK_SIZE_X = 100
DEFAULT_BLOCK_SIZE_Y = 40
COLOR_LIST = [
    (255, 140, 140), (140, 255, 140), (140, 140, 255), (255, 215, 140), 
    (200, 140, 255), (140, 255, 255), (255, 255, 140), (255, 140, 255), 
    (140, 255, 200), (255, 200, 140), (255, 140, 200), (200, 255, 140),
    (140, 200, 255), (200, 140, 200), (140, 200, 140), (200, 200, 255), 
    (215, 255, 140), (140, 255, 215), (255, 140, 215), (215, 140, 255), 
    (140, 215, 255), (255, 255, 200), (200, 255, 255), (255, 200, 255),
    (255, 215, 215), (215, 255, 215)
]
"""Predefined list of colors for blocks in RGB format"""


class BlockModel(BaseModel):
    """shared class for the input data that has to be provided for creating blocks"""
    name: str = Field(..., pattern=r'^[A-Z]$')
    x_size: Optional[int] = None
    y_size: Optional[int] = None
    weight: Optional[int] = None
    type: Optional[str] = None


class Block:
    """Represents a single block in the simulation.
    Handles the blocks properties and its visual apperance."""

    def __init__(
            self, 
            name: str, 
            color_index: Optional[int] = None,
            x_size: Optional[int] = DEFAULT_BLOCK_SIZE_X, 
            y_size: Optional[int] = DEFAULT_BLOCK_SIZE_Y, 
            weight: Optional[int] = None,
            type: Optional[str] = None,
            x_init: Optional[int] = 0, 
            y_init: Optional[int] = 0
            ):
        self._name = name
        """Block's name (usually a single letter A-Z)"""
        self._color = COLOR_LIST[color_index] if color_index is not None else COLOR_LIST[random.randint(0, len(COLOR_LIST) - 1)]
        """Block's color given as the index of COLOR_LIST - will be randomly selected if not provided"""
        self._x = x_init
        """Block's x position (center of the block)"""
        self._y = y_init
        """Block's y position (top of the block)"""
        self._width = x_size if x_size is not None else DEFAULT_BLOCK_SIZE_X
        """Block's width"""
        self._height = y_size if y_size is not None else DEFAULT_BLOCK_SIZE_Y
        """Block's height"""
        self._weight = weight
        """Block's weight"""
        self._type = type
        """Block's type"""

    def get_name(self) -> str:
        """Get the block's name"""
        return self._name
    
    def get_size(self) -> Tuple[int, int]:
        """Get the block's size (width, height)"""
        return self._width, self._height

    def get_position(self) -> Tuple[int, int]:
        """Get the current position of the block (center x, center y)"""
        return self._x, self._y

    def get_weight(self) -> int:
        """Get the block's weight"""
        return self._weight
    
    def get_type(self) -> str:
        """Get the block's type"""
        return self._type
    
    def to_dict(self) -> dict:
        """Convert the block to a dictionary representation"""
        out_dict: dict = {
            "name": self._name,
            "x_size": self._width,
            "y_size": self._height
        }
        if self._weight is not None:
            out_dict["weight"] = self._weight
        if self._type is not None:
            out_dict["type"] = self._type
        return out_dict

    def set_position(self, x: int, y: int):
        """Set the current position of the block(center x, center y)"""
        self._x = x
        self._y = y

    def set_position_on_robot(self, robot_x: int, robot_y: int):
        """Set the position of the block relative to the robot's position (center x, top y)"""
        self._x = robot_x
        self._y = robot_y + self._height // 2
        
    def draw(self, surface):
        """Draw the block on the given surface
        This method will be called by the stack if the block is stacked
        and by the robot if the block is held"""
        # Draw the block as a rectangle centered at (self._x, self._y)
        rect = pygame.Rect(
            self._x - self._width // 2,
            self._y - self._height // 2,
            self._width,
            self._height
        )
        corner_radius = 4
        # actual block
        pygame.draw.rect(
            surface,
            self._color,
            rect,
            border_radius=corner_radius
        )
        # border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            rect,
            width=2,
            border_radius=corner_radius
        )
        # Draw the block's name in the center (including weight)
        font = pygame.font.Font(None, 40)
        label = self._name
        details = []
        if self._weight is not None:
            details.append(f"W:{self._weight}")
        if self._type is not None:
            details.append(f"T:{self._type}")
        if details:
            label += " (" + "/".join(details) + ")"
        text_surface = font.render(label, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self._x, self._y))
        surface.blit(text_surface, text_rect)