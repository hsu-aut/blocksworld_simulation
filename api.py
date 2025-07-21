from flask import Flask, request, jsonify
import queue

app = Flask(__name__)
command_queue = queue.Queue()
status_queue = queue.Queue()
reply_queue = queue.Queue()

@app.route('/pick_up', methods=['POST'])
def pick_up():
    data = request.get_json()
    block = data.get('block')
    command_queue.put(('pick_up', block))
    return jsonify({"result": f"Command pick_up {block} queued."})

@app.route('/put_down', methods=['POST'])
def put_down():
    data = request.get_json()
    block = data.get('block')
    command_queue.put(('put_down', block))
    return jsonify({"result": f"Command put_down {block} queued."})

@app.route('/stack', methods=['POST'])
def stack():
    data = request.get_json()
    block1 = data.get('block1')
    block2 = data.get('block2')
    command_queue.put(('stack', block1, block2))
    return jsonify({"result": f"Command stack {block1} on {block2} queued."})

@app.route('/unstack', methods=['POST'])
def unstack():
    data = request.get_json()
    block1 = data.get('block1')
    block2 = data.get('block2')
    command_queue.put(('unstack', block1, block2))
    return jsonify({"result": f"Command unstack {block1} from {block2} queued."})

@app.route('/get_status', methods=['POST'])
def get_status():
    status_queue.put(('get_status',))
    try:
        status_received = reply_queue.get(timeout=2)
        return jsonify({"result": f"{status_received}"})
    except queue.Empty:
        return jsonify({"result": "No status available."})

@app.route('/check_free_stack', methods=['POST'])
def check_free_stack():
    status_queue.put(('check_free_stack',))
    try:
        status_received = reply_queue.get(timeout=2)
        return jsonify({"result": f"{status_received}"})
    except queue.Empty:
        return jsonify({"result": "No status available."})

def run_flask():
    app.run(port=5001, host='127.0.0.1', use_reloader=False, threaded=True)