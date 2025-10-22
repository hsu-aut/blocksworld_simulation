# 🧱 Blocksworld Simulation

A visual simulation environment for the classic Blocksworld AI planning problem. The simulation features a robot arm that can manipulate colored blocks across multiple stacks, with support for both interactive GUI control and programmatic access via a REST API.

## ✨ Features

- **Interactive GUI**: Pygame-based visual simulation with real-time block manipulation
- **REST API**: Complete Flask-based API for programmatic control and automation
- **Predefined Scenarios**: 20+ built-in challenges with varying difficulty levels
- **Plan Execution & Validation**: Test AI-generated plans before execution
- **Constraint Sets**: Multiple rule sets including standard blocksworld and Tower of Hanoi
- **Optimal Solutions**: Reference solutions provided for all scenarios
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

## 🎮 Control Methods

### Keyboard Control

- **Pick up/Unstack**: Press the letter of the block you want to pick up
- **Put down**: Press `SPACE` to place the held block on the ground
- **Stack**: While holding a block, press the letter of the target block to stack on top of it
- **Start random simulation**: Press `SPACE` (when no simulation is running)

### REST API Control

The API provides 13 endpoints for complete programmatic control:

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
- `POST /validate_plan` - Validate a plan without executing it

#### Information
- `GET /get_status` - Get current simulation state (blocks, stacks, robot)
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

# 3. Validate your plan before executing
curl -X POST http://127.0.0.1:5001/validate_plan \
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
- **`hanoi_towers`**: Tower of Hanoi rules (blocks must be placed in size order)

Specify the constraint set when starting a simulation:
```bash
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{"initial_stacks": [["A"], ["B"], ["C"]], "constraint_set": "hanoi_towers"}'
```

## 📚 Documentation

- [REST API Documentation](./docs/rest-api.md) - Complete API reference with examples
- Scenario definitions: `src/blocksworld_simulation/scenarios/definitions/`
