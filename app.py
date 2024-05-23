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

@app.route('/update_temp' , methods=['POST'])
def up():
    data = request.json
    value = data.get('temp_user', None)
    
    data = {
    "TRANSMISSION_PATH": {
        "TX": "BACKEND",
        "RX": "DEVICE",
        "BACKEND_DATA": {
            "APP_STATE": "OPEN",
            "AVERAGE_POWER_WATT": "KEEP",
            "ACTIVATION": "DONE",
            "WIFI_SETTING": "KEEP",
            "APP_DATA": {
                "MODE_DATA": {
                    "FEATURES": "TURBO",
                    "MODE": "COOL"
                },
                "COMPONENT_DATA": {
                    "PLASMA": "ON",
                    "FAN": "LOW",
                    "H_LOUVRE": "POS_1",
                    "V_LOUVRE": "POS_2"
                },
                "CONTROL_DATA": {
                    "TIMER_STATE": "OFF",
                    "TIMER_HOURS": "0",
                    "TEMP_CELSIUS_USER": value
                }
            }
        }
    }
}
    
    sent_message = json.dumps(data)

    try:
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_str)
        registry_manager.send_c2d_message(device_id, sent_message)
        print(sent_message)
        return jsonify({'message': f"Message {sent_message} sent successfully"})
    except msrest.exceptions.HttpOperationError as ex:
        return jsonify({'error': f"HttpOperationError: {ex.response.text}"})
    except Exception as ex:
        return jsonify({'error': f"Unexpected error: {ex}"})

def run_flask():
    app.run(debug=True)

if __name__ == '__main__':
    # Start the Flask server in the main thread
    run_flask()