# Blocksworld Simulation REST API Documentation

A Flask-based REST API for controlling a robotic arm in a blocks world simulation environment.

## Base URL
```
http://127.0.0.1:5001
```

## Endpoints

### 1. Pick Up Block
Picks up a block from the ground.

**Endpoint:** `POST /pick_up`

**Request Body:**
```json
{
  "block": "block_name"
}
```

**Response:**
```json
{
  "result": "Command pick_up block_name queued."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/pick_up \
  -H "Content-Type: application/json" \
  -d '{"block": "A"}'
```

### 2. Put Down Block
Puts down a held block on the ground.

**Endpoint:** `POST /put_down`

**Request Body:**
```json
{
  "block": "block_name"
}
```

**Response:**
```json
{
  "result": "Command put_down block_name queued."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/put_down \
  -H "Content-Type: application/json" \
  -d '{"block": "A"}'
```

### 3. Stack Blocks
Stacks block1 on top of block2.

**Endpoint:** `POST /stack`

**Request Body:**
```json
{
  "block1": "block_to_place",
  "block2": "block_base"
}
```

**Response:**
```json
{
  "result": "Command stack block_to_place on block_base queued."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/stack \
  -H "Content-Type: application/json" \
  -d '{"block1": "A", "block2": "B"}'
```

### 4. Unstack Blocks
Unstacks block1 from block2.

**Endpoint:** `POST /unstack`

**Request Body:**
```json
{
  "block1": "block_to_remove",
  "block2": "block_base"
}
```

**Response:**
```json
{
  "result": "Command unstack block_to_remove from block_base queued."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/unstack \
  -H "Content-Type: application/json" \
  -d '{"block1": "A", "block2": "B"}'
```

### 5. Get Status
Returns the current status from the robot and current positions of each block.

**Endpoint:** `POST /get_status`

**Request Body:** Empty JSON object
```json
{}
```

**Response:**
```json
{
  "result": "status_information"
}
```

**Error Response (timeout):**
```json
{
  "result": "No status available."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/get_status \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Check Free Stack
Checks for available free stack positions.

**Endpoint:** `POST /check_free_stack`

**Request Body:** Empty JSON object
```json
{}
```

**Response:**
```json
{
  "result": "free_stack_information"
}
```

**Error Response (timeout):**
```json
{
  "result": "No status available."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:5001/check_free_stack \
  -H "Content-Type: application/json" \
  -d '{}'
```