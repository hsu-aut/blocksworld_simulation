from typing import Optional, Tuple
import pygame


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
            color: Tuple[int, int, int],
            x_size: int, 
            y_size: int, 
            weight: int,
            type: str,
            x_init: Optional[int] = 0, 
            y_init: Optional[int] = 0
            ):
        self._name = name
        """Block's name (usually a single letter A-Z)"""
        self._color = color
        """Block's color in RGB format"""
        self._x = x_init
        """Block's x position (center of the block)"""
        self._y = y_init
        """Block's y position (top of the block)"""
        self._width = x_size
        """Block's width"""
        self._height = y_size
        """Block's height"""
        self._weight = weight
        """Block's weightr"""
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
        font = pygame.font.Font(None, 20)
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