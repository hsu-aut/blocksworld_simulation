def get_base_rules() -> str:
    return """# Blocksworld Environment Rules
## Overview
The blocksworld is a classic AI planning domain where a robot manipulates blocks in a simulated environment.

## Environment
- Blocks are labeled with letters (A, B, C, etc.)
- Blocks can be placed on the ground or stacked on top of other blocks
- Only one block can be on top of another block at any time
- The robot has a single gripper and can hold only one block at a time
- Limited Stack Positions: There is a maximum number of stack positions available on the ground

## Stack Positions Constraints
- The ground has a finite number of stack positions where blocks can be placed
- Each Stack Positions can support a stack of blocks
- No new Stack Positions can be created
- When all Stack Positions are occupied, blocks must be stacked vertically
- Strategic planning required when ground space is limited

## Robot States
- **Idle**: Robot is not holding any block (robot gripper is empty)
- **Holding**: Robot is holding exactly one block

## Block States
- **On Ground**: Block is directly on the ground surface of the stack position
- **Clear**: No other block is stacked on top of this block
- **Stacked**: Block is placed on top of another block

## Planning Constraints
- Only one action can be performed at a time
- All preconditions must be satisfied before an action can be executed
- Actions have deterministic effects
- The environment is fully observable
- Ground space is limited: 
    - plan stack arrangements carefully
    - Consider available Stack Positions when planning moves  
    - Some configurations may be impossible due to ground space limitations or block arrangements
    - Check current Stack Positions usage via get_status tool

## Goal Specification
Goals are typically specified as desired block arrangements, such as:
- "Stack A on B"
- "Put all blocks on the ground"
- "Create tower A-B-C from bottom to top"

## Available Actions
Use the provided MCP tools for block manipulation actions."""