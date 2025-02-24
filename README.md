# Warga Naget's Assignment 2 Samsung Innovation Campus Batch 2

## General Information
Nama Kelompok: Warga Naget
Kode Kelompok: UNI466

Anggota Kelompok:
- Deira Aisya Refani
- Finanazwa Ayesha
- Regina Joan Medea Jati Laksono
- Yusuf Imantaka Bastari

## Project Overview
This project involves developing a REST API using Flask to collect, store, and retrieve sensor data from an ESP32 device. The ESP32 collects temperature and humidity data and transmits it to the server, where it is stored in a MongoDB database. Additionally, the system includes a switch control feature, allowing remote toggling of a device via an Ubidots dashboard.

### Key Features
- Flask REST API:

Handles HTTP requests to store and retrieve sensor data.
Provides endpoints for temperature, humidity, and switch status.
- MongoDB Integration:

Stores real-time sensor data with timestamps.
Enables querying data based on time range.
- ESP32 Communication:

Sends temperature and humidity data to the API.
Fetches switch status from the API to control connected devices.
- Ubidots Dashboard Visualization:

Displays real-time and historical data for temperature and humidity.
Includes an on/off switch to control devices remotely.

### How It Works
1. The ESP32 device reads temperature and humidity values from sensors.
2. It sends the data to the Flask API via HTTP POST requests.
3. The API stores the data in MongoDB and provides GET endpoints for retrieval.
4. The Ubidots dashboard fetches sensor data from the API for visualization.
5. The user can toggle a switch on Ubidots, which updates the switch status in MongoDB.
6. The ESP32 periodically checks the switch status and performs actions accordingly.
7. This project demonstrates an end-to-end IoT solution integrating hardware (ESP32), backend (Flask API + MongoDB), and a cloud-based visualization platform (Ubidots).

Ubidots Link: https://stem.ubidots.com/app/dashboards/67bbb7edd878668cd9aa970f
\\

Video Demonstration Link: 
