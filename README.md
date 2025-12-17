# 🧱 Blocksworld Simulation

A visual simulation environment for the classic Blocksworld AI planning problem. The simulation features a robot arm that can manipulate colored blocks across multiple stacks, with support for both interactive GUI control and programmatic access via a REST API.

## ✨ Features

- **Interactive GUI**: Pygame-based visual simulation with real-time block manipulation
- **REST API**: Complete Flask-based API for programmatic control and automation
- **LLM-Ready**: Compatible with AI assistants through our [MCP Server](https://github.com/hsu-aut/llmstudy_mcp-server)
- **Predefined Scenarios**: 50 built-in challenges across 5 categories with varying difficulty levels
- **Plan Execution & Verification**: Test AI-generated plans before execution
- **Constraint Sets**: Multiple rule sets including standard blocksworld, size-based constraints, and partial observability
- **Keyboard Control**: Quick manual testing and experimentation

## 🚀 Quick Start

### Installation

The project uses [Poetry](https://python-poetry.org/docs/#installation) for dependency management.

1. Clone the repository:
```bash
git clone <repository-url>
cd blocksworld-simulation
```

2. Install dependencies:
```bash
poetry install
```

3. Run the simulation:
```bash
poetry run blocksworld-simulation
```

The GUI will open, and the REST API will be available at `http://127.0.0.1:5001`.

## 🤖 LLM Integration

Want to use this simulation with your own AI agents or just try it out with LLMs like Claude or ChatGPT? Check out our **[MCP Server for Blocksworld Simulation](https://github.com/hsu-aut/llmstudy_mcp-server)** that exposes the simulation as MCP tools.

The MCP server allows LLMs to:
- Interact with the simulation through natural language
- Execute block manipulation actions as tool calls
- Query the simulation state and rules
- Verify and execute multi-step plans

Perfect for AI planning research, testing LLM reasoning capabilities, or building AI agents!

## 🎮 Control Methods

### Keyboard Control

- **Start random simulation**: Press `SPACE` (when no simulation is running)
- **Pick up/Unstack**: Press the letter of the block you want to pick up
- **Put down**: Press `SPACE` to place the held block on the ground
- **Stack**: While holding a block, press the letter of the target block to stack on top of it
- **Stop simulation**: Press `ESC` to stop the current simulation and start a new one

### REST API Control

The API provides 14 endpoints for complete programmatic control:

#### Simulation Control
- `POST /start_simulation` - Start with a scenario or custom configuration
- `POST /stop_simulation` - Stop the current simulation
- `POST /quit` - Quit the application

#### Block Actions
- `POST /pick_up` - Pick up a block from the ground
- `POST /put_down` - Put down a held block
- `POST /stack` - Stack one block on another
- `POST /unstack` - Unstack one block from another

#### Plan Execution
- `POST /execute_plan` - Execute a sequence of actions with GUI animation
- `POST /verify_plan` - Verify a plan without executing it

#### Information
- `GET /get_status` - Get current simulation state (respects partial observability)
- `GET /get_full_status` - Get complete simulation state (bypasses partial observability)
- `GET /get_rules` - Get active constraint rules
- `GET /scenarios` - List all available scenarios
- `GET /scenarios/<name_or_id>` - Get details for a specific scenario

For detailed API documentation with request/response examples, see the [REST API Documentation](./docs/rest-api.md).

## 📋 Example Workflow

```bash
# 1. Get a scenario with its optimal plan
curl http://127.0.0.1:5001/scenarios/Tower%20Building%20Challenge

# 2. Start the scenario
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "Tower Building Challenge"}'

# 3. Verify your plan before executing
curl -X POST http://127.0.0.1:5001/verify_plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"}
    ]
  }'

# 4. Execute the plan (watch it in the GUI!)
curl -X POST http://127.0.0.1:5001/execute_plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"}
    ]
  }'
```

## 🎯 Constraint Sets

The simulation supports different rule sets:

- **`base`** (default): Standard blocksworld with limited ground positions
- **`block_size`**: Blocks with varying sizes - blocks can only be placed on larger or equal-sized blocks
- **`partial_observability`**: Limited visibility of simulation state

Specify the constraint set when starting a simulation:
```bash
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{"initial_stacks": [["A"], ["B"], ["C"]], "constraint_set": "block_size"}'
```

## 📚 Documentation

- [REST API Documentation](./docs/rest-api.md) - Complete API reference with examples
- [MCP Server Repository](https://github.com/hsu-aut/llmstudy_mcp-server) - LLM integration via Model Context Protocol
- Scenario definitions: `src/blocksworld_simulation/scenarios/definitions/`

## 🔗 Related Projects

- **[Blocksworld MCP Server](https://github.com/hsu-aut/llmstudy_mcp-server)** - Enable LLMs to control the simulation through MCP tools
