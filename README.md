# 🤖 Box World Simulation  

the project compares the Capabilities & Skills approach vs AI Agents for planning and task execution. 
---

## 🧱 Blocksworld (Pygame)

A minimal 2D grid environment built with Pygame. It serves as a simple testbed for agents to navigate, interact with boxes, and complete basic tasks.

### Run it:

```bash
python blocksworld.py
```
### Control:

**Controlling the Robot with Keyboard:**
Press the letter of a corresponding block to pick it up. (When controlling via the keyboard, there's no distinction made between unstack and pickup)

When a block is lifted, it can either be placed on the floor (put down) using the space bar or stacked on another block by typing the corresponding letter of the block (stack).

**Controlling the Robot via the MCP server:**
The MCP-Server has 5 tools:

1. pick_up(block):
    picks up a block from the ground

2. put_down(block):
    puts down a held block on the ground

3. stack(block1, block2):
    stacks block1 on top of block2

4. unstack(block1, block2):
    unstacks block1 from block2

5. getstatus():
    returns the current status from the robot as well as the current positions of each block
