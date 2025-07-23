from flask import Flask, request, jsonify
import queue
import threading

app = Flask(__name__)
api_in_queue = queue.Queue()
api_out_queue = queue.Queue()
simulation_thread = None

def return_api(result):
    """Helper function to format API responses and print before returning."""
    print(f" API <-- {result}")
    return jsonify({"result": result})

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    """Start the pygame simulation with optional configuration."""
    data = request.get_json(silent=True) or {}
    initial_stacks = data.get('initial_stacks')
    box_number = data.get('box_number')

    from blocksworld_simulation.simulation.simulation import start_pygame_mainloop

    global simulation_thread
    if simulation_thread and simulation_thread.is_alive():
        return return_api('Simulation already running.')

    simulation_thread = threading.Thread(
        target=start_pygame_mainloop,
        kwargs={'initial_setup': initial_stacks, 'num_boxes': box_number}
    )
    simulation_thread.daemon = True
    simulation_thread.start()
    return return_api('Simulation started.')

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    """Stop the pygame simulation."""
    global simulation_thread
    from blocksworld_simulation.simulation import simulation
    if simulation_thread and simulation_thread.is_alive():
        # This is a placeholder; actual implementation to stop pygame is needed
        simulation.stop_simulation = True
        simulation_thread.join(timeout=5)
        return return_api('Simulation stopped.')
    
    return return_api('No simulation running.')

@app.route('/pick_up', methods=['POST'])
def pick_up():
    data = request.get_json()
    block = data.get('block')
    api_in_queue.put(('pick_up', block))
    result = api_out_queue.get()
    return return_api(result)

@app.route('/put_down', methods=['POST'])
def put_down():
    data = request.get_json()
    block = data.get('block')
    api_in_queue.put(('put_down', block))
    result = api_out_queue.get()
    return return_api(result)

@app.route('/stack', methods=['POST'])
def stack():
    data = request.get_json()
    block1 = data.get('block1')
    block2 = data.get('block2')
    api_in_queue.put(('stack', block1, block2))
    result = api_out_queue.get()
    return return_api(result)

@app.route('/unstack', methods=['POST'])
def unstack():
    data = request.get_json()
    block1 = data.get('block1')
    block2 = data.get('block2')
    api_in_queue.put(('unstack', block1, block2))
    result = api_out_queue.get()
    return return_api(result)

@app.route('/get_status', methods=['GET'])
def get_status():
    api_in_queue.put(('get_status',))
    result = api_out_queue.get()
    return return_api(result)

@app.route('/check_free_stack', methods=['GET'])
def check_free_stack():
    api_in_queue.put(('check_free_stack',))
    result = api_out_queue.get()
    return return_api(result)

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False)