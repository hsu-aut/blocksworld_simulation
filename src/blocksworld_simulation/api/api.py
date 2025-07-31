from flask import Flask, jsonify
import queue
import logging

from ..simulation.simulation_input import (
    GetStatusInput, StartInput, StopInput, PickUpInput, PutDownInput, StackInput, UnstackInput
)
from .request_validation import (
    validate_request, StartSimulationRequest, PickUpRequest, PutDownRequest,
    StackRequest, UnstackRequest
)

app = Flask(__name__)
api_to_sim_queue = queue.Queue()
sim_to_api_queue = queue.Queue()
logger = logging.getLogger(__name__)

def return_api(result):
    """Helper function to format API responses and print before returning."""
    success, message = result
    if success:
        logger.info(f" API 200 <-- {message}")
    else:
        logger.warning(f" API 4xx <-- {message}")
    return jsonify({"result": message}), 200 if success else 400

@app.route('/start_simulation', methods=['POST'])
@validate_request(StartSimulationRequest, allow_empty_body=True)
def start_simulation(validated_data: StartSimulationRequest):
    """Start the pygame simulation with optional configuration."""
    api_to_sim_queue.put(StartInput(
        reply_queue=sim_to_api_queue,
        stack_config=validated_data.initial_stacks if validated_data else None
    ))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    """Stop the pygame simulation."""
    api_to_sim_queue.put(StopInput(reply_queue=sim_to_api_queue))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/pick_up', methods=['POST'])
@validate_request(PickUpRequest)
def pick_up(validated_data: PickUpRequest):
    api_to_sim_queue.put(PickUpInput(
        reply_queue=sim_to_api_queue,
        block_name=validated_data.block
    ))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/put_down', methods=['POST'])
@validate_request(PutDownRequest)
def put_down(validated_data: PutDownRequest):
    api_to_sim_queue.put(PutDownInput(
        reply_queue=sim_to_api_queue,
        block_name=validated_data.block 
    ))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stack', methods=['POST'])
@validate_request(StackRequest)
def stack(validated_data: StackRequest):
    api_to_sim_queue.put(StackInput(
        reply_queue=sim_to_api_queue,
        block_name=validated_data.block1, 
        target_block_name=validated_data.block2
    ))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/unstack', methods=['POST'])
@validate_request(UnstackRequest)
def unstack(validated_data: UnstackRequest):
    api_to_sim_queue.put(UnstackInput(
        reply_queue=sim_to_api_queue,
        block_name=validated_data.block1, 
        block_below_name=validated_data.block2
    ))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/get_status', methods=['GET'])
def get_status():
    api_to_sim_queue.put(GetStatusInput(reply_queue=sim_to_api_queue))
    result = sim_to_api_queue.get()
    return return_api(result)

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False)