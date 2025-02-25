from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)

# Koneksi ke MongoDB
uri = "mongodb+srv://deiraaisyarefani:mmWW6Ep5k6MMbb2P@cluster0.oe0jv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['MyDatabase']
my_collections = db['SensorData']

# Fungsi untuk menyimpan data ke MongoDB
def store_data(data):
    result = my_collections.insert_one(data)
    print(f"Data stored with id: {result.inserted_id}")
    return str(result.inserted_id)

# Endpoint untuk menerima data dari ESP32
@app.route('/sensor1', methods=['POST'])
def simpan_data_sensor():
    try:
        body = request.get_json()
        temperature = body.get('temperature')
        humidity = body.get('humidity')
        switch = body.get('switch')
        led_status = body.get('led_status')

        if None in (temperature, humidity, switch, led_status):
            return jsonify({"error": "Missing data"}), 400

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        data_final = {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp,
            'switch': switch,
            'led_status': led_status
        }

        id = store_data(data_final)
        return jsonify({"message": f"Data stored successfully with id: {id}"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mengirim status LED ke ESP32
@app.route('/get_led_status', methods=['GET'])
def get_led_status():
    try:
        latest_data = my_collections.find_one(sort=[("_id", -1)])  # Ambil data terbaru
        if latest_data:
            return jsonify({"led_status": latest_data.get('led_status', 0)}), 200
        else:
            return jsonify({"led_status": 0}), 200  # Default jika tidak ada data

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
