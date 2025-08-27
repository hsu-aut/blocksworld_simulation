import random
from typing import List, Optional
import logging

from .block import Block, BlockModel
from .stack import Stack


logger = logging.getLogger(__name__)

STACK_TO_BORDER_OFFSET = 50
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
STACK_BASE_HEIGHT = 20
STACK_BASE_WIDTH = 100
DEFAULT_N_BLOCKS = 4
DEFAULT_N_STACKS = 3

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
    color_indexes = random.sample(range(26), n_blocks)
    for i in range(n_blocks):
        block = Block(
            name=chr(65 + i), # name: A, B, C, ...
            color_index=color_indexes[i]
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
    # else, get number of blocks and stacks
    n_stacks = len(stack_config)
    n_blocks = sum(len(stack) for stack in stack_config)
    # create random index
    color_indexes = random.sample(range(26), n_blocks)
    color_indexes_index = 0
    # create empty stacks
    stacks = create_empty_stacks(n_stacks)
    # iterate over stacks and blocks
    for i, stack in enumerate(stack_config):
        for block_data in stack:
            block: Block = None
            # if only a string is given, create a block with the string as its name
            # and default values for everything else
            if isinstance(block_data, str):
                block = Block(
                    name=block_data, 
                    color_index=color_indexes[color_indexes_index]
                )
            # else, use data provided in dict
            elif isinstance(block_data, BlockModel):
                block = Block(
                    name=block_data.name,
                    color_index=color_indexes[color_indexes_index],
                    x_size=block_data.x_size,
                    y_size=block_data.y_size,
                    weight=block_data.weight,
                    type=block_data.type
                )
            color_indexes_index += 1
            block.set_position(stacks[i].get_x(), stacks[i].get_top_y()-block.get_size()[1] // 2)
            stacks[i].add_block(block)
    return stacks