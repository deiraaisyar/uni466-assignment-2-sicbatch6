from flask import Flask, jsonify, request
app = Flask(__name__)

from statistics import mean
from datetime import datetime

# pymongo Section
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://deiraaisyarefani:mmWW6Ep5k6MMbb2P@cluster0.oe0jv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to server
client = MongoClient(uri, server_api=ServerApi('1'))

# Make a database
db = client['MyDatabase'] 
my_collections = db['SensorData']

def store_data(data):
    results = my_collections.insert_one(data)
    print(f"Data stored with id: {results.inserted_id}")
    return results.inserted_id
    
def get_temperature():
    get_temperature_result = my_collections.find({}, {'_id':0, 'temperature':1, 'timestamp':1})
    return get_temperature_result

def get_humidity():
    get_humidity_result = my_collections.find({}, {'_id':0, 'humidity':1})
    return get_humidity_result

@app.route('/', methods=['GET'])
def entry_point():
    return jsonify({"message": "Welcome to our API"})

@app.route('/sensor1', methods=['POST','GET'])
def simpan_data_sensor():
    if request.method == 'POST':
        body = request.get_json()
        temperature = body['temperature']
        humidity = body['humidity']
        timestamp = body['timestamp']
        switch = body['switch']
        data_final = {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp,
            'switch': switch
        }
        
        id = store_data(data_final)
        return {
            "message": f"Data stored successfully with id: {id}"
        }

@app.route('/sensor1/temperature/all', methods=['GET'])
def get_data_temperature():
    result = [x for x in get_temperature()]
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    try:
        start_date_timestamp = datetime.strptime(start_date, "%d-%m-%Y %H:%M:%S")
        end_date_timestamp = datetime.strptime(end_date, "%d-%m-%Y %H:%M:%S")
        temp_list = []
        for items in result:
            print("cheking...")
            element = datetime.strptime(items['timestamp'], "%d-%m-%Y %H:%M:%S")
            if start_date_timestamp < element < end_date_timestamp:
                temp_list.append(items)
    
        return jsonify(message="Success", data=temp_list)
    
    except:
        pass
        
if __name__ == "__main__":
    app.run(debug=True, port=7000)
