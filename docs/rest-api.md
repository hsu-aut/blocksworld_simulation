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
Executes a sequence of actions as a plan.

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

#### 9. Validate Plan
Validates a plan without executing it.

**Endpoint:** `POST /validate_plan`

**Request Body:** Same format as execute_plan

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/validate_plan \
  -H "Content-Type: application/json" \
  -d '{"plan": [{"action": "pick_up", "block": "A"}]}'
```

### Information Endpoints

#### 10. Get Status
Returns the current simulation status and block positions.

**Endpoint:** `GET /get_status`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/get_status
```

#### 11. Get Rules
Returns the current constraint rules.

**Endpoint:** `GET /get_rules`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/get_rules
```

#### 12. List Scenarios
Lists all available scenarios.

**Endpoint:** `GET /scenarios`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/scenarios
```

#### 13. Get Scenario Details
Gets details for a specific scenario.

**Endpoint:** `GET /scenarios/<scenario_name>`

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:5001/scenarios/simple_tower
```