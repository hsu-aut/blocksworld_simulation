import random
from typing import List, Optional
import logging

from .block import Block
from .stack import Stack


logger = logging.getLogger(__name__)

STACK_TO_BORDER_OFFSET = 50
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
STACK_BASE_HEIGHT = 20
STACK_BASE_WIDTH = 100
DEFAULT_N_BLOCKS = 3
DEFAULT_N_STACKS = 2
DEFAULT_BLOCK_SIZE_X = 100
DEFAULT_BLOCK_SIZE_Y = 60
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

def get_random_colors(n_colors: int) -> list:
    """Return a list of n random colors from a predefined list of 26 colors."""
    return random.sample(COLOR_LIST, min(n_colors, len(COLOR_LIST)))

def create_empty_stacks(n_stacks: int) -> List[Stack]:
    """Create a list of empty stacks for the simulation"""
    stacks: List[Stack] = []
    stack_offset = (SCREEN_WIDTH - 2 * STACK_TO_BORDER_OFFSET - STACK_BASE_WIDTH) // (n_stacks - 1)
    for i in range(n_stacks):
        x = STACK_TO_BORDER_OFFSET + STACK_BASE_WIDTH // 2 + i * stack_offset
        stack = Stack(x, i, [])
        stacks.append(stack)
    return stacks

def create_random_stacks(n_blocks: int, n_stacks: int) -> List[Stack]:
    """Create a list of random stacks for the simulation"""
    # create n_blocks blocks
    blocks: List[Block] = []
    colors = get_random_colors(n_blocks)
    for i in range(n_blocks):
        block_name = chr(65 + i)  # name = A, B, C, ...
        color = colors[i % len(colors)]
        block = Block(
            name=block_name, 
            color=color, 
            x_size=DEFAULT_BLOCK_SIZE_X, 
            y_size=DEFAULT_BLOCK_SIZE_Y, 
            weight=None,
            type=None
        )
        blocks.append(block)
    # Create stacks and distribute blocks randomly
    stacks = create_empty_stacks(n_stacks)
    for block in blocks:
        stack = random.choice(stacks)
        block.set_position(
            stack.get_x(), 
            stack.get_top_y() - block.get_size()[1] // 2
        )
        stack.add_block(block)
    return stacks

def create_stacks(
        stack_config = None, 
        n_blocks: Optional[int] = DEFAULT_N_BLOCKS, 
        n_stacks: Optional[int] = DEFAULT_N_STACKS
        ) -> List[Stack]:
    """Create stacks based on input configuration."""
    if stack_config is None:
        # Create random stacks if no configuration is provided
        return create_random_stacks(n_blocks, n_stacks)
    logger.debug(f"Creating stacks with configuration: {stack_config}")
    n_stacks = len(stack_config)
    n_blocks = sum(len(stack) for stack in stack_config)
    colors = get_random_colors(n_blocks)
    color_index = 0
    # create empty stacks
    stacks = create_empty_stacks(n_stacks)
    for i, stack in enumerate(stack_config):
        for block_data in stack:
            block: Block = None
            if isinstance(block_data, str):
                block = Block(
                    name=block_data, 
                    color=colors[color_index], 
                    x_size=DEFAULT_BLOCK_SIZE_X, 
                    y_size=DEFAULT_BLOCK_SIZE_Y, 
                    weight=None, 
                    type=None
                )
            elif isinstance(block_data, dict):
                block = Block(
                    name=block_data.get("name"),
                    color=colors[color_index],
                    x_size=block_data.get("x_size", DEFAULT_BLOCK_SIZE_X),
                    y_size=block_data.get("y_size", DEFAULT_BLOCK_SIZE_Y),
                    weight=block_data.get("weight", None),
                    type=block_data.get("type", None)
                )
            if block is None:
                logger.warning(f"Invalid block data: {block_data}")
                continue
            color_index += 1
            block.set_position(stacks[i].get_x(), stacks[i].get_top_y()-block.get_size()[1] // 2)
            stacks[i].add_block(block)
    return stacks