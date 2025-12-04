# Blocksworld Simulation REST API Documentation

A Flask-based REST API for controlling a robotic arm in a blocks world simulation environment.

## Base URL
```
http://127.0.0.1:5001
```

## General Response Format
All endpoints return responses in the following format:
```json
{
  "result": "response_data"
}
```

Success responses return HTTP status 200, while errors return HTTP status 400.

### Success Response Example
```json
{
  "result": "Simulation started successfully"
}
```

### Error Response Example
```json
{
  "result": "Could not pick up block A - Block A is not clear"
}
```

## Constraint Sets
The simulation supports different constraint sets that define the rules for block manipulation:

- **`base`** (default): Standard blocksworld rules with limited ground positions
- **`hanoi_towers`**: Special rules for Tower of Hanoi puzzle (blocks must be placed in size order)

The active constraint set can be specified when starting a simulation with a scenario or custom configuration.

## Validation Rules
- Block names must be single uppercase letters (A-Z)
- All POST endpoints validate request data using Pydantic models

## Endpoints

### Simulation Control

#### 1. Start Simulation
Starts the simulation with either a predefined scenario or custom configuration.

**Endpoint:** `POST /start_simulation`

**Request Body (Optional):**
```json
{
  "scenario_id": "scenario_name"
}
```

**OR**

```json
{
  "initial_stacks": [["A", "B"], [], ["C"]],
  "constraint_set": "constraint_set_name"
}
```

**OR**

```json
{
  "initial_stacks": [
    [
      {"name": "D", "x_size": 100, "y_size": 30},
      {"name": "C", "x_size": 80, "y_size": 30}
    ],
    [],
    []
  ],
  "constraint_set": "hanoi_towers"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "simple_tower"}'
```

**Success Response:**
```json
{
  "result": "Simulation started successfully"
}
```

**Error Response:**
```json
{
  "result": "Could not start simulation - Unknown scenario"
}
```

#### 2. Stop Simulation
Stops the current simulation.

**Endpoint:** `POST /stop_simulation`

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/stop_simulation
```

#### 3. Quit Application
Quits the entire application.

**Endpoint:** `POST /quit`

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/quit
```

### Block Actions

#### 4. Pick Up Block
Picks up a block from the ground or stack.

**Endpoint:** `POST /pick_up`

**Request Body:**
```json
{
  "block": "A"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/pick_up \
  -H "Content-Type: application/json" \
  -d '{"block": "A"}'
```

#### 5. Put Down Block
Puts down a held block on the ground.

**Endpoint:** `POST /put_down`

**Request Body:**
```json
{
  "block": "A"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/put_down \
  -H "Content-Type: application/json" \
  -d '{"block": "A"}'
```

#### 6. Stack Blocks
Stacks block1 on top of block2.

**Endpoint:** `POST /stack`

**Request Body:**
```json
{
  "block1": "A",
  "block2": "B"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/stack \
  -H "Content-Type: application/json" \
  -d '{"block1": "A", "block2": "B"}'
```

#### 7. Unstack Blocks
Unstacks block1 from block2.

**Endpoint:** `POST /unstack`

**Request Body:**
```json
{
  "block1": "A",
  "block2": "B"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/unstack \
  -H "Content-Type: application/json" \
  -d '{"block1": "A", "block2": "B"}'
```

### Plan Execution

#### 8. Execute Plan
Executes a sequence of actions as a plan. The plan is executed in the GUI with visual animation of the robot's movements.

**Endpoint:** `POST /execute_plan`

**Request Body:**
```json
{
  "plan": [
    {
      "action": "pick_up",
      "block": "A"
    },
    {
      "action": "stack",
      "block1": "A",
      "block2": "B"
    },
    {
      "action": "unstack",
      "block1": "A",
      "block2": "B"
    },
    {
      "action": "put_down",
      "block": "A"
    }
  ]
}
```

**Available Actions:**
- `pick_up`: Requires `block` parameter
- `put_down`: Requires `block` parameter
- `stack`: Requires `block1` and `block2` parameters
- `unstack`: Requires `block1` and `block2` parameters

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/execute_plan \
  -H "Content-Type: application/json" \
  -d '{"plan": [{"action": "pick_up", "block": "A"}, {"action": "put_down", "block": "A"}]}'
```

#### 9. Verify Plan
Verifies a plan without executing it. The verification runs in the background without GUI animation and doesn't modify the actual simulation state. It checks if each action in the plan would be valid when executed sequentially.

**Endpoint:** `POST /verify_plan`

**Request Body:** Same format as execute_plan

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/verify_plan \
  -H "Content-Type: application/json" \
  -d '{"plan": [{"action": "pick_up", "block": "A"}]}'
```

**Success Response:**
```json
{
  "result": "Simulation plan is verified and can be executed."
}
```

**Error Response (Invalid Plan):**
```json
{
  "result": "Plan is invalid: Step 2: action='stack' block1='A' block2='B' Reason: Block B is not clear"
}
```

### Information Endpoints

#### 10. Get Status
Returns the current simulation status including all block positions, stack configurations, and robot state.

**Endpoint:** `GET /get_status`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/get_status
```

**Response Example:**
```json
{
  "result": {
    "stacks": [
      {
        "number": 1,
        "blocks": [
          {"name": "A", "x_size": 100, "y_size": 60, "position": 0},
          {"name": "B", "x_size": 100, "y_size": 60, "position": 1}
        ]
      },
      {
        "number": 2,
        "blocks": []
      },
      {
        "number": 3,
        "blocks": [
          {"name": "C", "x_size": 100, "y_size": 60, "position": 0}
        ]
      }
    ],
    "robot": {
      "state": "idle",
      "held_block": null
    }
  }
}
```

**Robot States:**
- `idle`: Robot is not holding any block
- `holding`: Robot is holding a block (check `held_block` for the block name)

#### 11. Get Rules
Returns the general blocksworld rules, including current constraint rules for the active constraint set in markdown format. This provides a human-readable description of all rules and constraints that apply to the current simulation.

**Endpoint:** `GET /get_rules`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/get_rules
```

**Response Example:**
```json
{
  "result": "# Blocksworld Environment Rules\n## Overview\nThe blocksworld is a classic AI planning domain...\n\n## Available Actions\nUse the provided MCP tools for block manipulation actions."
}
```

The response contains markdown-formatted text describing:
- Environment rules (blocks, stacks, robot capabilities)
- Ground position constraints
- Robot and block states
- Planning constraints
- Goal specification format
- Available actions

#### 12. List Scenarios
Lists all available predefined scenarios with their complete configuration including initial state, goal, and optimal plans.

**Endpoint:** `GET /scenarios`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/scenarios
```

**Response Example:**
```json
{
  "result": {
    "scenarios": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Tower Building Challenge",
        "description": "Rearrange blocks from 2 stacks to build tower B-A-C",
        "initial_state": {
          "stacks": [["A", "B"], ["C"], []],
          "holding": null,
          "robot_status": "idle"
        },
        "goal": {
          "description": "Build tower B-A-C",
          "target_configurations": [[], [], ["B", "A", "C"]]
        },
        "constraint_set": "base",
        "metadata": {
          "difficulty": "0",
          "min_steps": 6,
          "non_constructive_steps": 0,
          "num_blocks": 3,
          "num_stacks": 3
        },
        "optimal_plan": [
          {"action": "unstack", "block1": "B", "block2": "A"},
          {"action": "put_down", "block": "B"},
          {"action": "pick_up", "block": "A"},
          {"action": "stack", "block1": "A", "block2": "B"},
          {"action": "pick_up", "block": "C"},
          {"action": "stack", "block1": "C", "block2": "A"}
        ]
      }
    ]
  }
}
```

**Scenario Fields:**
- `id`: Unique identifier (UUID) for the scenario
- `name`: Human-readable name
- `description`: Brief description of the challenge
- `initial_state`: Starting configuration (stacks, robot state)
- `goal`: Target configuration to achieve
- `constraint_set`: Which constraint set to use (`base` or `hanoi_towers`)
- `metadata`: Additional information (difficulty level, optimal step count, etc.)
- `optimal_plan`: A known optimal solution (can be used for validation or as a reference)

#### 13. Get Scenario Details
Gets details for a specific scenario by name or ID.

**Endpoint:** `GET /scenarios/<scenario_name_or_id>`

**Parameters:**
- `scenario_name_or_id`: Can be either the scenario's unique ID (UUID) or its name

**cURL Examples:**
```bash
# By name
curl -X GET http://127.0.0.1:5001/scenarios/Tower%20Building%20Challenge

# By ID
curl -X GET http://127.0.0.1:5001/scenarios/550e8400-e29b-41d4-a716-446655440000
```

**Response Example:**
```json
{
  "result": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Tower Building Challenge",
    "description": "Rearrange blocks from 2 stacks to build tower B-A-C",
    "initial_state": {
      "stacks": [["A", "B"], ["C"], []],
      "holding": null,
      "robot_status": "idle"
    },
    "goal": {
      "description": "Build tower B-A-C",
      "target_configurations": [[], [], ["B", "A", "C"]]
    },
    "constraint_set": "base",
    "metadata": {
      "difficulty": "0",
      "min_steps": 6,
      "non_constructive_steps": 0,
      "num_blocks": 3,
      "num_stacks": 3
    },
    "optimal_plan": [
      {"action": "unstack", "block1": "B", "block2": "A"},
      {"action": "put_down", "block": "B"},
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"},
      {"action": "pick_up", "block": "C"},
      {"action": "stack", "block1": "C", "block2": "A"}
    ]
  }
}
```

**Error Response (Scenario Not Found):**
```json
{
  "result": "Could not retrieve scenario information - Unknown scenario"
}
```

---

## Common Error Messages

### Simulation State Errors
- `"Could not start simulation - Unknown scenario"`: The specified scenario ID does not exist
- `"Could not start simulation - Invalid constraint set"`: The specified constraint set is not available
- `"Could not start simulation - Simulation is already running"`: A simulation is already active

### Block Action Errors
- `"Could not pick up block A - Block A is not clear"`: Another block is stacked on top of block A
- `"Could not pick up block A - Robot is already holding a block"`: Robot must put down current block first
- `"Could not pick up block A - Block A does not exist"`: Block A is not in the simulation
- `"Could not put down block A - Robot is not holding block A"`: Robot must be holding the specified block
- `"Could not put down block A - No available ground positions"`: All ground positions are occupied
- `"Could not stack block A on block B - Robot is not holding block A"`: Must pick up block A first
- `"Could not stack block A on block B - Block B is not clear"`: Another block is already on top of B
- `"Could not unstack block A from block B - Block A is not on top of block B"`: Blocks are not in specified configuration
- `"Could not unstack block A from block B - Block A is not clear"`: Another block is on top of A

### Plan Execution Errors
- `"Plan is invalid at step N - <error message>"`: The plan fails at the Nth action with the specified error
- `"Invalid action type in plan"`: An unrecognized action type was specified in the plan
- `"Missing required parameters for action"`: Action is missing `block`, `block1`, or `block2` parameters

### Hanoi Towers Specific Errors
When using the `hanoi_towers` constraint set:
- `"Could not stack block A on block B - Larger blocks cannot be placed on smaller blocks"`: Violates Tower of Hanoi rule

---

## Usage Examples

### Starting a Scenario and Executing Its Optimal Plan
```bash
# 1. Start with a specific scenario
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "550e8400-e29b-41d4-a716-446655440000"}'

# 2. Get the scenario details to see the optimal plan
curl -X GET http://127.0.0.1:5001/scenarios/550e8400-e29b-41d4-a716-446655440000

# 3. Execute the optimal plan from the scenario
curl -X POST http://127.0.0.1:5001/execute_plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"action": "unstack", "block1": "B", "block2": "A"},
      {"action": "put_down", "block": "B"},
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"},
      {"action": "pick_up", "block": "C"},
      {"action": "stack", "block1": "C", "block2": "A"}
    ]
  }'
```

### Verifying a Plan Before Execution
```bash
# Verify a plan to check if it would work
curl -X POST http://127.0.0.1:5001/verify_plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"}
    ]
  }'

# If valid, execute it
curl -X POST http://127.0.0.1:5001/execute_plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan": [
      {"action": "pick_up", "block": "A"},
      {"action": "stack", "block1": "A", "block2": "B"}
    ]
  }'
```

### Custom Simulation with Hanoi Towers Rules
```bash
curl -X POST http://127.0.0.1:5001/start_simulation \
  -H "Content-Type: application/json" \
  -d '{
    "initial_stacks": [
      [
        {"name": "C", "x_size": 120, "y_size": 30},
        {"name": "B", "x_size": 100, "y_size": 30},
        {"name": "A", "x_size": 80, "y_size": 30}
      ],
      [],
      []
    ],
    "constraint_set": "hanoi_towers"
  }'
```