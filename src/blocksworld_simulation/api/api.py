from flask import Flask, jsonify
import queue
import logging

from ..simulation.simulation_actions import (
    GetRulesAction, GetStatusAction, PreStartAction, StopAction, PickUpAction, PutDownAction, StackAction, UnstackAction, GetScenariosAction
)
from .request_validation import (
    validate_request, validate_params
)
from .request_models import (
    StartSimulationRequest, StopSimulationRequest,
    PickUpRequest, PutDownRequest, StackRequest, UnstackRequest,
    ScenarioRequest, GetStatusRequest, GetRulesRequest
)

app = Flask(__name__)
api_to_sim_queue = queue.Queue()
sim_to_api_queue = queue.Queue()
logger = logging.getLogger(__name__)

def return_api(result):
    """Helper function to format API responses and log before returning."""
    success, message = result
    if success:
        logger.info(f" API 200 <-- {message}")
    else:
        logger.warning(f" API 400 <-- {message}")
    return jsonify({"result": message}), 200 if success else 400

@app.route('/start_simulation', methods=['POST'])
@validate_request(StartSimulationRequest, allow_empty_body=True)
def start_simulation(validated_data: StartSimulationRequest):
    """Start the pygame simulation with scenario or custom configuration."""
    api_to_sim_queue.put(PreStartAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stop_simulation', methods=['POST'])
@validate_request(StopSimulationRequest)
def stop_simulation(validated_data: StopSimulationRequest):
    """Stop the pygame simulation."""
    api_to_sim_queue.put(StopAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/pick_up', methods=['POST'])
@validate_request(PickUpRequest)
def pick_up(validated_data: PickUpRequest):
    api_to_sim_queue.put(PickUpAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/put_down', methods=['POST'])
@validate_request(PutDownRequest)
def put_down(validated_data: PutDownRequest):
    api_to_sim_queue.put(PutDownAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stack', methods=['POST'])
@validate_request(StackRequest)
def stack(validated_data: StackRequest):
    api_to_sim_queue.put(StackAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/unstack', methods=['POST'])
@validate_request(UnstackRequest)
def unstack(validated_data: UnstackRequest):
    api_to_sim_queue.put(UnstackAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/scenarios', methods=['GET'])
@validate_params(ScenarioRequest)
def list_scenarios(validated_data: ScenarioRequest):
    """Get list of all available scenarios."""
    api_to_sim_queue.put(GetScenariosAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/scenarios/<scenario_name>', methods=['GET'])
@validate_params(ScenarioRequest)
def get_scenario_details(validated_data: ScenarioRequest):
    """Get detailed information about a specific scenario."""
    api_to_sim_queue.put(GetScenariosAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/get_status', methods=['GET'])
@validate_params(GetStatusRequest)
def get_status(validated_data: GetStatusRequest):
    api_to_sim_queue.put(GetStatusAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/get_rules', methods=['GET'])
@validate_params(GetRulesRequest)
def get_rules(validated_data: GetRulesRequest):
    api_to_sim_queue.put(GetRulesAction(sim_to_api_queue, validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False)