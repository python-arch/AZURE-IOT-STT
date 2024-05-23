from flask import Flask, jsonify
from flask import request
from azure.iot.hub import IoTHubRegistryManager
import msrest
import json

app = Flask(__name__)


connection_str = "HostName=rd-iothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=TcpaortpcdjcMkZDre1kVhBMdkAZVUXYPAIoTPaN/kQ="
device_id = "TND_WH_10521C663374"


@app.route('/up', methods=['POST'])
def up():
    # Extract the value from the POST request body
    data = request.json
    value = data.get('temp_user', None)  # Assuming the value is sent as a JSON object with a key 'value'
    features = data.get('features',None)
    mode = data.get('mode', None)
    plasma = data.get('plasma', None)
    fan = data.get('fan', None)
    h_louvre = data.get('h_louvre', None)
    v_louvre = data.get('v_louvre',None)
    timer_state = data.get('timer_state' , None)
    timer_hours = data.get('timer_hours', None)
    

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
                    "FEATURES": features,
                    "MODE": mode
                },
                "COMPONENT_DATA": {
                    "PLASMA": plasma,
                    "FAN": fan,
                    "H_LOUVRE": h_louvre,
                    "V_LOUVRE": v_louvre
                },
                "CONTROL_DATA": {
                    "TIMER_STATE": timer_state,
                    "TIMER_HOURS": timer_hours,
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


@app.route('/down', methods=['POST'])
def down():
    data = request.json
    value = data.get('temp_user', None)  # Assuming the value is sent as a JSON object with a key 'value'
    features = data.get('features',None)
    mode = data.get('mode', None)
    plasma = data.get('plasma', None)
    fan = data.get('fan', None)
    h_louvre = data.get('h_louvre', None)
    v_louvre = data.get('v_louvre',None)
    timer_state = data.get('timer_state' , None)
    timer_hours = data.get('timer_hours', None)
    
    
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
                    "FEATURES": features,
                    "MODE": mode,
                },
                "COMPONENT_DATA": {
                    "PLASMA": plasma,
                    "FAN": fan,
                    "H_LOUVRE": h_louvre,
                    "V_LOUVRE": v_louvre,
                },
                "CONTROL_DATA": {
                    "TIMER_STATE": timer_state,
                    "TIMER_HOURS":timer_hours,
                    "TEMP_CELSIUS_USER": value,
                }
            }
        }
    }
}
    sent_message = json.dumps(data)
    try:
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_str)
        registry_manager.send_c2d_message(device_id, sent_message)
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