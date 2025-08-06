from typing import List
from .block import Block
import pygame

STACK_BASE_WIDTH = 100
STACK_BASE_HEIGHT = 20
SCREEN_HEIGHT = 600


class Stack:
    """Represents a stack where blocks can be placed.
    Handles stacking/unstacking operation and the visual apperance of the stack."""

    def __init__(self, x: int, number: int, initial_blocks: List[Block]):
        self._x = x
        self._number = number
        self._blocks: List[Block] = initial_blocks

    def add_block(self, block: Block):
        """Add a block to the top of this stack"""
        self._blocks.append(block)
    
    def get_blocks(self) -> List[Block]:
        """Get all blocks in this stack"""
        return self._blocks

    def remove_top_block(self):
        """Remove a block from this stack if it's on top"""
        self._blocks.remove(self._blocks[-1])
        return

    def get_x(self) -> int:
        """Get the x position of the stack"""
        return self._x
    
    def get_top_y(self) -> int:
        """Get the y position where the next block should be placed"""
        if not self._blocks:
            return SCREEN_HEIGHT - STACK_BASE_HEIGHT
        else:
            top_block = self._blocks[-1]
            top_block_height = top_block.get_size()[1]
            top_block_y = top_block.get_position()[1]
            return top_block_y - top_block_height // 2
        
    def get_number(self) -> int:
        """Get the stack number"""
        return self._number + 1  # Stack numbers are 1-indexed for user-friendliness
    
    def to_dict(self) -> dict:
        """Convert the stack to a dictionary representation"""
        blocks_with_positions = []
        for position, block in enumerate(self._blocks):
            block_dict = block.to_dict()
            block_dict["position"] = position
            blocks_with_positions.append(block_dict)
        
        out_dict: dict = {
            "number": self.get_number(),
            "blocks": blocks_with_positions
        }
        return out_dict

    def draw(self, surface):
        """Draw the stack and its blocks on the given surface"""
        # Draw the base of the stack
        pygame.draw.rect(
            surface,
            (100, 100, 100),  # Base color = gray
            (
                self._x - STACK_BASE_WIDTH // 2,
                SCREEN_HEIGHT - STACK_BASE_HEIGHT,
                STACK_BASE_WIDTH,
                STACK_BASE_HEIGHT
            )
        )
        # Draw stack label
        font = pygame.font.Font(None, 18)
        label = f"Stack {self.get_number()}"
        text_surface = font.render(label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self._x, SCREEN_HEIGHT - STACK_BASE_HEIGHT // 2))
        surface.blit(text_surface, text_rect)
        # draw all blocks in the stack
        for block in self._blocks:
            block.draw(surface)