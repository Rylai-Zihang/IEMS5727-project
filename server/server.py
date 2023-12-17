from flask import Flask, request, jsonify
from db import Database
from keepalive import KeepAlive
import os
import atexit


app = Flask(__name__)

with app.app_context():
    global db
    username = os.getenv('USER')
    db = Database("localhost", "5432", "iot", username, "")
    db.connect()

    global kl
    kl = KeepAlive()

def teardown_database():
    global db
    if db:
        db.disconnect()
        db = None

atexit.register(teardown_database)

@app.route('/api/keepalive', methods=['POST'])
def keepalive():
    device = request.form.get('device', '')
    device_type = request.form.get('type', '')
    time = request.form.get('timestamp', '')
    global kl
    kl.keepalive(device, device_type, time)
    return jsonify({'device': device, 'message': 'keepalive'}), 200


@app.route('/api/upload/fire', methods=['POST'])
def upload_fire():
    if 'image' not in request.files:
        return jsonify({'error': 'Invalid request'}), 400
    device = request.form.get('device', '')
    image_file = request.files['image'].read()
    conf_value = request.form.get('conf', '')
    detected_at = request.form.get('timestamp', '')
    global db
    db.insert_fire_data(device, image_file, conf_value, int(detected_at))
    return jsonify({'message': 'fire received and processed'}), 200

@app.route('/api/upload/temperature', methods=['POST'])
def upload_temperature():
    device = request.form.get('device', '')
    temperature_value = request.form.get('temperature', '')
    detected_at = request.form.get('timestamp', '')
    global db
    db.insert_temperature_data(device, temperature_value, int(detected_at))
    return jsonify({'message': 'temperature received and processed'}), 200

@app.route('/api/query/recent_fires/<int:num_records>', methods=['GET'])
def query_recent_fires(num_records):
    global db
    recent_fires = db.get_recent_fires_with_images(num_records)
    return jsonify(recent_fires), 200

@app.route('/api/query/analyse_data', methods=['GET'])
def query_analyse_data():
    global db
    log_data = db.get_recent_fires_with_images(5)
    device_warning_data = db.get_device_warning_data()
    temperature_data = db.get_recent_device_tempeature_data(10)
    total_data = db.get_total_fires_count()
    risk_data = [
        {
          "name": "Device A",
          "value": 78
        },
        {
          "name": "Device B",
          "value": 38
        },
        {
          "name": "Device C",
          "value": 46
        },
        {
          "name": "Device D",
          "value": 36
        },
        {
          "name": "Device E",
          "value": 89
        }
    ]
    global kl
    status_data = kl.get_status()
    response = {
        'status':200,
        'data':{
            'deviceWarningData':device_warning_data,
            'logData':log_data,
            'riskData':risk_data,
            'totalData':total_data,
            'temperatureData':temperature_data,
            'aliveData':status_data,
        }
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000) 
