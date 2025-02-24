from flask import Flask, jsonify, request
app = Flask(__name__)

from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://deiraaisyarefani:mmWW6Ep5k6MMbb2P@cluster0.oe0jv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['MyDatabase'] 
my_collections = db['SensorData']

def store_data(data):
    results = my_collections.insert_one(data)
    print(f"Data stored with id: {results.inserted_id}")
    return results.inserted_id

def get_temperature():
    return my_collections.find({}, {'_id': 0, 'temperature': 1, 'timestamp': 1})

def get_humidity():
    return my_collections.find({}, {'_id': 0, 'humidity': 1})

def get_switch_status():
    # Ambil data switch terbaru berdasarkan timestamp terbaru
    latest_switch = my_collections.find_one({}, {'_id': 0, 'switch': 1}, sort=[("timestamp", -1)])
    return latest_switch['switch'] if latest_switch else "Unknown"

@app.route('/', methods=['GET'])
def entry_point():
    return jsonify({"message": "Welcome to our API"})

@app.route('/sensor1', methods=['POST', 'GET'])
def simpan_data_sensor():
    if request.method == 'POST':
        body = request.get_json()
        temperature = body.get('temperature')
        humidity = body.get('humidity')
        timestamp = body.get('timestamp')
        switch = body.get('switch')

        if None in (temperature, humidity, timestamp, switch):
            return jsonify({"error": "Missing data"}), 400

        data_final = {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp,
            'switch': switch
        }

        id = store_data(data_final)
        return jsonify({"message": f"Data stored successfully with id: {id}"})

@app.route('/sensor1/temperature/all', methods=['GET'])
def get_data_temperature():
    result = list(get_temperature())
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    try:
        start_date_timestamp = datetime.strptime(start_date, "%d-%m-%Y %H:%M:%S")
        end_date_timestamp = datetime.strptime(end_date, "%d-%m-%Y %H:%M:%S")
        temp_list = []

        for items in result:
            element = datetime.strptime(items['timestamp'], "%d-%m-%Y %H:%M:%S")
            if start_date_timestamp < element < end_date_timestamp:
                temp_list.append(items)

        return jsonify(message="Success", data=temp_list)
    
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'DD-MM-YYYY HH:MM:SS'"}), 400

@app.route('/sensor1/switch/status', methods=['GET'])
def get_switch():
    switch_status = get_switch_status()
    return jsonify({"switch_status": switch_status})

if __name__ == "__main__":
    app.run(debug=True, port=7000)

