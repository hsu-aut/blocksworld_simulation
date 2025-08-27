from blocksworld_simulation.simulation.simulation_state import SimulationState
import pygame
from typing import List
import logging
from queue import Queue

from .simulation_input import SimulationInput, QuitInput, StartInput, StopInput, PickUpInput, PutDownInput, StackInput, UnstackInput

from .robot import Robot, RobotState
from .stack import Stack

logger = logging.getLogger(__name__)

def handle_user_inputs(
        reply_queue: Queue,
        simulation_state: SimulationState
    ) -> SimulationInput | None:
    """Handle pygame inputs by the user. Returns a SimulationInput or None.
    This method only checks basic conditions and constraints.
    Other checks are done in the input processor (which is also respronsible for API inputs)."""
    # get values
    simulation_running: bool = simulation_state.get_simulation_running()
    robot: Robot = simulation_state.get_robot()
    stacks: List[Stack] = simulation_state.get_stacks()
    # check for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logger.info("Quit input received")
            return QuitInput(reply_queue=reply_queue)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                logger.info("<SPACE> key pressed")
                if simulation_running:
                    # if <SPACE> is pressed and simulation is running, create a put down input
                    return PutDownInput(
                        block_name=robot.get_held_block().get_name() if robot.get_held_block() else None,
                        reply_queue=reply_queue)
                else:
                    # if <SPACE> is pressed and simulation is not running, create a start input
                    return StartInput(reply_queue=reply_queue)
            elif event.key == pygame.K_ESCAPE:
                logger.info("<ESCAPE> key pressed")
                # if <ESCAPE> is pressed, create a stop input
                return StopInput(reply_queue=reply_queue)
            else:
                key_name = pygame.key.name(event.key)
                if len(key_name) == 1 and key_name.isalpha() and simulation_running:
                    if robot.get_state() == RobotState.IDLE:
                        logger.info(f"<{key_name.upper()}> key pressed")
                        # find stack, block and block position in stack based on key_name
                        for stack in stacks:
                            for block in stack.get_blocks():
                                if block.get_name().upper() == key_name.upper():
                                    i_block = stack.get_blocks().index(block)
                                    block_below = stack.get_blocks()[i_block - 1] if i_block > 0 else None
                                    logger.debug(f"Found stack: {stack.get_number()}, block: {block.get_name()}, block_below: {block_below.get_name() if block_below else None}")
                                    # if a <KEY> is pressed and block <KEY> is on a stack with only one block, create a pick up input
                                    if len(stack.get_blocks()) == 1:
                                        return PickUpInput(
                                            block_name=key_name.upper(),
                                            reply_queue=reply_queue
                                        )
                                    # if a <KEY> is pressed and block <KEY> is on another block and robot is idle, create a unstack input
                                    else:
                                        return UnstackInput(
                                            block_name=key_name.upper(),
                                            block_below_name=block_below.get_name() if block_below else None,
                                            reply_queue=reply_queue
                                        )
                    elif robot.get_state() == RobotState.HOLDING:
                        logger.info(f"<{key_name.upper()}> key pressed")
                        # if a <KEY> is pressed and robot is holding a block, create a stack input, 
                        # block currently being held on block <KEY>
                        return StackInput(
                            block_name=robot.get_held_block().get_name(),
                            target_block_name=key_name.upper(),
                            reply_queue=reply_queue
                        )
                    else:
                        logger.warning(f"<{key_name.upper()}> key pressed but robot is not idle or holding a block")
                        return None
                elif len(key_name) == 1 and key_name.isalpha() and not simulation_running:
                    logger.warning(f"<{key_name.upper()}> key pressed but simulation is not running")
                    return None
    return None