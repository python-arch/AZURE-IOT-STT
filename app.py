from flask import Flask, jsonify
from flask import request
from azure.iot.hub import IoTHubRegistryManager
import msrest
import json

app = Flask(__name__)


connection_str = "HostName=rd-iothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=TcpaortpcdjcMkZDre1kVhBMdkAZVUXYPAIoTPaN/kQ="
device_id = "TND_WH_10521C663374"

@app.route('/')
def index():
    return jsonify({'message': 'Connected to the server'})

@app.route('/up')
def up():
    sent_message = "1"
    try:
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_str)
        registry_manager.send_c2d_message(device_id, sent_message)
        return jsonify({'message': f"Message up sent successfully"})
    except msrest.exceptions.HttpOperationError as ex:
        return jsonify({'error': f"HttpOperationError: {ex.response.text}"})
    except Exception as ex:
        return jsonify({'error': f"Unexpected error: {ex}"})

@app.route('/down')
def down():
    sent_message = "0"
    try:
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_str)
        registry_manager.send_c2d_message(device_id, sent_message)
        return jsonify({'message': f"Message down sent successfully"})
    except msrest.exceptions.HttpOperationError as ex:
        return jsonify({'error': f"HttpOperationError: {ex.response.text}"})
    except Exception as ex:
        return jsonify({'error': f"Unexpected error: {ex}"})
    
def run_flask():
    app.run(debug=True)

if __name__ == '__main__':
    # Start the Flask server in the main thread
    run_flask()