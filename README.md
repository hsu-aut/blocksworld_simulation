# 🧱 Blocksworld Simulation (Pygame)

In this project, a simulation is provided with which the classic Blocksworld problem can be represented / simulated. 
For this purpose, a robot arm is simulated that can place and move colored boxes on different stacks.  
The graphical simulation is based on Pygame and several actions can be controlled either via keyboard input or conveniently via a REST API with Flask.

## How to run

The project uses the [Poetry](https://python-poetry.org/docs/#installation) dependency management.
Clone the repository and execute:

```bash
poetry install
```

to install the required packages.
Then, run the simulation by executing: 

```bash
poetry run python blocksworld.py
```

## Control

### Controlling the Robot with Keyboard

Press the letter of a corresponding block to pick it up. 
When controlling via the keyboard, there's no distinction made between unstack and pickup.

When a block is lifted, it can either be placed on the floor (put down) using the space bar or stacked on another block by typing the corresponding letter of the block (stack).

### Controlling the Robot via REST API commands

There are the following 5 commands:

1. `pick_up(block)` - picks up a block from the ground

2. `put_down(block)` - puts down a held block on the ground

3. `stack(block1, block2)` - stacks block1 on top of block2

4. `unstack(block1, block2)` - unstacks block1 from block2

5. `get_status()` - returns the current status from the robot as well as the current positions of each block

For detailed information about the available REST API endpoints and example requests, see the [API documentation](./simulation/rest-api.md).

### Controlling the Robot via MCP

There is also an MCP server [`mcp_server.py`](./mcp/mcp_server.py) that provides tools to control the robot via the REST API using the commands mentioned. 
The tools of the MCP server interact directly with the REST endpoints and thus also enable an AI or external programs to control the robot and receive feedback.
