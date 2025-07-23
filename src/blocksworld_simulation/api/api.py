from flask import Flask, request, jsonify
import queue
import threading

app = Flask(__name__)
api_in_queue = queue.Queue()
api_out_queue = queue.Queue()

def return_api(result):
    """Helper function to format API responses and print before returning."""
    print(f" API <-- {result}")
    return jsonify({"result": result})

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
    app.run(port=5001, host='127.0.0.1', use_reloader=False, threaded=True)

def start_flask_thread():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()