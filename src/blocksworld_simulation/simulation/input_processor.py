from blocksworld_simulation.simulation.simulation_state import SimulationState
from .robot import RobotState, Robot
from .block import Block
from .stack import Stack
import logging
from typing import List
from .simulation_action import SimulationAction, StartAction, StopAction, QuitAction, PickUpAction, PutDownAction, StackAction, UnstackAction, GetStatusAction
from .simulation_input import SimulationInput, StartInput, StopInput, QuitInput, PickUpInput, PutDownInput, StackInput, UnstackInput, GetStatusInput


logger = logging.getLogger(__name__)

def process_input(
        simulation_input: SimulationInput,
        simulation_state: SimulationState
    ) -> SimulationAction | str:
    """Process inputs from the user or API and return a SimulationAction object.
    This method checks all relevant conditions/constraints and returns an appropriate action only if it is executable.
    In any other case, it returns None."""

    # get values
    simulation_running: bool = simulation_state.get_simulation_running()
    robot: Robot = simulation_state.get_robot()
    stacks: List[Stack] = simulation_state.get_stacks()
    robot_held_block: Block = robot.get_held_block() if robot is not None else None
    blocks: List[Block] = [block for stack in stacks for block in stack.get_blocks()] if stacks else []
    blocks.append(robot_held_block if robot_held_block else None) 

    # QUIT
    if isinstance(simulation_input, QuitInput):
        # log the input
        logger.info("Input processor: quit input received")
        # if a quit input is received, return a quit action in any case
        return QuitAction(reply_queue=simulation_input.get_reply_queue())
    
    # START
    elif isinstance(simulation_input, StartInput):
        # log the input
        logger.info(f"Input processor: start input received: {simulation_input.get_stack_config()}")
        # CHECK 1 --- if  simulation is already running, deny the input
        if simulation_running:
            simulation_input.reply(success=False, message=f"Start input denied, as simulation is already running.")
            return None
        # if no deny reason was triggered, return a StartAction with the stack configuration
        return StartAction(
            reply_queue=simulation_input.get_reply_queue(), 
            stack_config=simulation_input.get_stack_config()
        )

    # STOP
    elif isinstance(simulation_input, StopInput):
        # log the input
        logger.info("Input processor: stop input received")
        # CHECK 1 --- if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Stop input denied, as simulation is not running.")
            return None
        # if no deny reason was triggered, return a StopAction
        return StopAction(reply_queue=simulation_input.get_reply_queue())
    
    # GET STATUS
    elif isinstance(simulation_input, GetStatusInput):
        # log the input
        logger.info("Input processor: get status input received")
        # CHECK 1 --- if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Get status input denied, as simulation is not running.")
            return None
        # if no deny reason was triggered, return a GetStatusAction
        return GetStatusAction(reply_queue=simulation_input.get_reply_queue())

    # PICK UP    
    elif isinstance(simulation_input, PickUpInput):
        # get the block name from the input
        block_name = simulation_input.get_block_name()
        # log the input
        logger.info(f"Input processor: pick up input received for block {block_name}")
        # CHECK 1 --- if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Pick up input denied, as simulation is not running.")
            return None
        # CHECK 2 ---  if robot is not idle, deny the input
        if robot.get_state() != RobotState.IDLE:
            simulation_input.reply(success=False, message=f"Pick up input denied, as robot is not idle.")
            return None
        # CHECK 3 ---  if the block does not exist, deny the input
        if not any(block.get_name() == block_name for block in blocks):
            simulation_input.reply(success=False, message=f"Pick up input denied, as block {block_name} does not exist in the simulation.")
            return None
        # find the stack and the block
        block: Block = None
        stack: Stack = None
        for _stack in stacks:
            for _block in _stack.get_blocks():
                if _block.get_name() == block_name:
                    # CHECK 4 ---  if the stack does not have only one block, deny the input
                    if len(_stack.get_blocks()) > 1:
                        simulation_input.reply(success=False, message=f"Pick up input denied, as block {block_name} is not on the ground.")
                        return None
                    # CHECK 5 ---  if the block is not on top of the stack, deny the input
                    if not _stack.get_blocks()[-1].get_name() == block_name:
                        simulation_input.reply(success=False, message=f"Pick up input denied, as block {block_name} is not on top of a stack.")
                        return None
                    block = _block
                    stack = _stack
                    break
        # if no deny reason was triggered, return a PickUpAction with the stack
        return PickUpAction(
            reply_queue=simulation_input.get_reply_queue(),
            block=block,
            stack=stack
        )

    # PUT DOWN
    elif isinstance(simulation_input, PutDownInput):
        # get the block name from the input
        block_name = simulation_input.get_block_name()
        # log the input
        logger.info(f"Input processor: put down input received for block {block_name}")
        # CHECK 1 ---  if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Put down input denied, as simulation is not running.")
            return None
        # CHECK 2 ---  if robot is not holding a block, deny the input
        if robot.get_state() != RobotState.IDLE and robot.get_state() != RobotState.HOLDING:
            simulation_input.reply(success=False, message=f"Put down input denied, as robot is not available.")
            return None
        # CHECK 2 ---  if robot is not holding a block, deny the input
        if robot.get_state() != RobotState.HOLDING:
            simulation_input.reply(success=False, message=f"Put down input denied, as robot is not holding a block.")
            return None
        # CHECK 3 ---  if the block does not exist, deny the input
        if not any(block.get_name() == block_name for block in blocks):
            simulation_input.reply(success=False, message=f"Put down input denied, as block {block_name} does not exist in the simulation.")
            return None
        # CHECK 4 ---  if the robot is not holding the block, deny the input
        if robot_held_block.get_name() != block_name:
            simulation_input.reply(success=False, message=f"Put down input denied, as robot is not holding block {block_name}.")
            return None
        # find a free stack to put down the block
        stack: Stack = None
        for _stack in stacks:
            if not _stack.get_blocks():
                stack = _stack
                break
        # CHECK 5 ---  if no free stack is found, deny the input
        if stack is None:
            simulation_input.reply(success=False, message=f"Put down input denied, as no free stack is available.")
            return None
        # if no deny reason was triggered, return a PutDownAction
        return PutDownAction(
            reply_queue=simulation_input.get_reply_queue(),
            block=robot_held_block,
            stack=stack
        )

    # STACK
    elif isinstance(simulation_input, StackInput):
        # get the block and target block names from the input
        block_name = simulation_input.get_block_name()
        target_block_name = simulation_input.get_target_block_name()
        # log the input
        logger.info(f"Input processor: stack input received for block {block_name} to stack on {target_block_name}")
        # CHECK 1 --- if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Stack input denied, as simulation is not running.")
            return None
        # CHECK 2 --- if robot is not holding a block, deny the input
        if robot.get_state() != RobotState.HOLDING:
            simulation_input.reply(success=False, message=f"Stack input denied, as robot is not holding a block.")
            return None
        # CHECK 3 --- if the block does not exist, deny the input
        if not any(block.get_name() == block_name for block in blocks):
            simulation_input.reply(success=False, message=f"Stack input denied, as block {block_name} does not exist in the simulation.")
            return None
        # CHECK 4 --- if the robot is not holding the block, deny the input
        if robot_held_block.get_name() != block_name:
            simulation_input.reply(success=False, message=f"Stack input denied, as robot is not holding block {block_name}.")
            return None
        # CHECK 5 --- if the target block does not exist, deny the input
        if not any(block.get_name() == target_block_name for block in blocks):
            simulation_input.reply(success=False, message=f"Stack input denied, as target block (block {target_block_name}) does not exist in the simulation.")
            return None
        # find the target stack and block
        target_block: Block = None
        target_stack: Stack = None
        for _target_stack in stacks:
            for _target_block in _target_stack.get_blocks():
                if _target_block.get_name() == target_block_name:
                    # CHECK 6 --- if the target block is not on top of the stack, deny the input
                    if not _target_stack.get_blocks()[-1].get_name() == target_block_name:
                        simulation_input.reply(success=False, message=f"Stack input denied, as target block {target_block_name} is not on top of a stack.")
                        return None
                    target_block = _target_block
                    target_stack = _target_stack
                    break
        # if no deny reason was triggered, return a StackAction with the target block and stack
        return StackAction(
            reply_queue=simulation_input.get_reply_queue(),
            block=robot_held_block,
            stack=target_stack,
            target_block=target_block
        )

    # UNSTACK
    elif isinstance(simulation_input, UnstackInput):
        # get the block and target block names from the input
        block_name = simulation_input.get_block_name()
        block_below_name = simulation_input.get_block_below_name()
        # log the input
        logger.info(f"Input processor: unstack input received for block {block_name} to unstack from {block_below_name}")
        # CHECK 1 ---  if the simulation is not running, deny the input
        if not simulation_running:
            simulation_input.reply(success=False, message=f"Unstack input denied, as simulation is not running.")
            return None
        # CHECK 2 ---  if robot is not idle, deny the input
        if robot.get_state() != RobotState.IDLE:
            simulation_input.reply(success=False, message=f"Unstack input denied, as robot is not idle.")
            return None
        # CHECK 3 ---  if the block does not exist, deny the input
        if not any(block.get_name() == block_name for block in blocks):
            simulation_input.reply(success=False, message=f"Unstack input denied, as block {block_name} does not exist in the simulation.")
            return None
        # find the stack and the block
        block: Block = None
        stack: Stack = None
        for _stack in stacks:
            for _block in _stack.get_blocks():
                if _block.get_name() == block_name:
                    # CHECK 4 ---  if the block is not on top of the stack, deny the input
                    if not _stack.get_blocks()[-1].get_name() == block_name:
                        simulation_input.reply(success=False, message=f"Unstack input denied, as block {block_name} is not on top of a stack.")
                        return None
                    block = _block
                    stack = _stack
                    break
        # CHECK 5 ---  if the target block does not exist, deny the input
        if not any(block.get_name() == block_below_name for block in blocks):
            simulation_input.reply(success=False, message=f"Unstack input denied, as block below (block {block_below_name}) does not exist in the simulation.")
            return None
        # find the block below and its stack
        block_below: Block = None
        block_below_stack: Stack = None
        for _block_below_stack in stacks:
            for _block_below in _block_below_stack.get_blocks():
                if _block_below.get_name() == block_below_name:
                    # CHECK 6 ---  if the block below is on a different stack, deny the input
                    if _block_below_stack != stack:
                        simulation_input.reply(success=False, message=f"Unstack input denied, as block {block_below_name} is not on the same stack as block {block_name}.")
                        return None
                    # CHECK 7 ---  if the block below is not below the block, deny the input
                    if not _block_below_stack.get_blocks().index(_block_below) == stack.get_blocks().index(block) - 1:
                        simulation_input.reply(success=False, message=f"Unstack input denied, as block {block_below_name} is not below block {block_name}.")
                        return None
                    block_below = _block_below
                    block_below_stack = _block_below_stack
                    break
        # if no deny reason was triggered,return an UnstackAction
        return UnstackAction(
            reply_queue=simulation_input.get_reply_queue(),
            block=block,
            stack=stack,
            block_below=block_below
        )

    # if no valid input is received, return None (should not happen)
    simulation_input.reply(success=False, message=f"Received an invalid input - returning None - THIS SHOULD NOT HAPPEN")
    return None