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
from ..scenarios.scenario_manager import scenario_manager

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
    """Start the pygame simulation with optional scenario or individual stack configuration."""
    scenario = None
    stack_config = None
    
    if validated_data:
        if validated_data.scenario:
            scenario = scenario_manager.get_scenario(validated_data.scenario)
            if not scenario:
                return jsonify({"error": f"Scenario '{validated_data.scenario}' not found"}), 404
            
            # Use provided initial_stacks if given, otherwise use scenario's initial state
            stack_config = validated_data.initial_stacks if validated_data.initial_stacks else scenario.initial_state.stacks
        else:
            # Only initial_stacks provided (no scenario)
            stack_config = validated_data.initial_stacks
    
    api_to_sim_queue.put(StartInput(
        reply_queue=sim_to_api_queue,
        stack_config=stack_config
    ))
    result = sim_to_api_queue.get()
    
    if scenario and result[0]:  # If scenario was used and simulation started successfully
        return jsonify({
            "result": result[1],
            "scenario": {
                "name": scenario.name,
                "description": scenario.description,
                "goal": scenario.goal.model_dump()
            }
        }), 200
    
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

@app.route('/scenarios', methods=['GET'])
def list_scenarios():
    """Get list of all available scenarios."""
    scenarios = []
    for name in scenario_manager.get_scenario_names():
        scenario = scenario_manager.get_scenario(name)
        if scenario:
            scenarios.append(scenario.model_dump())
    return jsonify({"scenarios": scenarios}), 200

@app.route('/scenarios/<scenario_name>', methods=['GET'])
def get_scenario_details(scenario_name: str):
    """Get detailed information about a specific scenario."""
    scenario = scenario_manager.get_scenario(scenario_name)
    if not scenario:
        return jsonify({"error": f"Scenario '{scenario_name}' not found"}), 404

    return jsonify(scenario.model_dump()), 200

@app.route('/get_status', methods=['GET'])
def get_status():
    api_to_sim_queue.put(GetStatusInput(reply_queue=sim_to_api_queue))
    result = sim_to_api_queue.get()
    return return_api(result)

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False)