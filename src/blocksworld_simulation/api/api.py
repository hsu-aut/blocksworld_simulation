import json
from flask import Flask, jsonify
import queue
import logging

from blocksworld_simulation.simulation.simulation_actions import (
    PreStartAction, QuitAction, StopAction,
    PickUpAction, PutDownAction, StackAction, UnstackAction, 
    ExecutePlanAction, VerifyPlanAction,
    GetScenarioAction, GetStatusAction, GetRulesAction
)

from .request_validation import validate_request
from .request_models import (
    StartSimulationRequest,
    PickUpRequest, PutDownRequest, StackRequest, UnstackRequest,
    PlanRequest
)


app = Flask(__name__)
api_to_sim_queue = queue.Queue()
sim_to_api_queue = queue.Queue()
logger = logging.getLogger(__name__)

def return_api(result):
    """Helper function to format API responses and log before returning."""
    success, message = result
    if success:
        logger.info(f" API 200 <-- {json.dumps(message, indent=1)}")
    else:
        logger.warning(f" API 400 <-- {json.dumps(message, indent=1)}")
    return jsonify({"result": message}), 200 if success else 400

@app.route('/start_simulation', methods=['POST'])
@validate_request(StartSimulationRequest, allow_empty_body=True)
def start_simulation(validated_data: StartSimulationRequest):
    api_to_sim_queue.put(PreStartAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/quit', methods=['POST'])
def quit_simulation():
    api_to_sim_queue.put(QuitAction())
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    api_to_sim_queue.put(StopAction())
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/pick_up', methods=['POST'])
@validate_request(PickUpRequest)
def pick_up(validated_data: PickUpRequest):
    api_to_sim_queue.put(PickUpAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/put_down', methods=['POST'])
@validate_request(PutDownRequest)
def put_down(validated_data: PutDownRequest):
    api_to_sim_queue.put(PutDownAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/stack', methods=['POST'])
@validate_request(StackRequest)
def stack(validated_data: StackRequest):
    api_to_sim_queue.put(StackAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/unstack', methods=['POST'])
@validate_request(UnstackRequest)
def unstack(validated_data: UnstackRequest):
    api_to_sim_queue.put(UnstackAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/execute_plan', methods=['POST'])
@validate_request(PlanRequest)
def execute_plan(validated_data: PlanRequest):
    api_to_sim_queue.put(ExecutePlanAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/verify_plan', methods=['POST'])
@validate_request(PlanRequest)
def verify_plan(validated_data: PlanRequest):
    api_to_sim_queue.put(VerifyPlanAction(validated_data))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/scenarios', methods=['GET'])
def list_scenarios():
    api_to_sim_queue.put(GetScenarioAction())
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/scenarios/<scenario_name>', methods=['GET'])
def get_scenario_details(scenario_name: str):
    api_to_sim_queue.put(GetScenarioAction(scenario_name))
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/get_status', methods=['GET'])
def get_status():
    api_to_sim_queue.put(GetStatusAction())
    result = sim_to_api_queue.get()
    return return_api(result)

@app.route('/get_rules', methods=['GET'])
def get_rules():
    api_to_sim_queue.put(GetRulesAction())
    result = sim_to_api_queue.get()
    return return_api(result)

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False, debug=True)