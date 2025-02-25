import machine
import network
import ujson
import utime as time
import dht
import urequests as requests

# === KONFIGURASI ===
WIFI_SSID = "WISMA 2003 NEW TENGAH"
WIFI_PASSWORD = "K1N4NT1NEW"
UBIDOTS_TOKEN = "BBUS-GDzt8RZBsPVXE7AsGy6LNigiIWqnTN"
UBIDOTS_DEVICE = "ESP32-SIC6"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE}/"
FLASK_SERVER_URL = "http://192.168.0.108:7000/sensor1"

# === KONFIGURASI PIN ESP32 ===
DHT_PIN = 23
LED_PIN = 22
BUTTON_PIN = 4

# Inisialisasi sensor dan komponen
dht_sensor = dht.DHT22(machine.Pin(DHT_PIN))
led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# === KONEKSI KE WIFI ===
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
print("Menghubungkan ke WiFi...")

while not wifi.isconnected():
    time.sleep(1)
    print("Menghubungkan...")

print("WiFi Terhubung:", wifi.ifconfig())

# === FUNGSI AMBIL STATUS LED DARI UBIDOTS ===
def get_led_status():
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    try:
        response = requests.get(f"{UBIDOTS_URL}led_status/lv", headers=headers)
        if response.status_code == 200:
            return int(float(response.text))
    except Exception as e:
        print("Gagal mengambil status LED dari Ubidots:", e)
    return None  

# === FUNGSI AMBIL STATUS SWITCH DARI UBIDOTS ===
def get_switch_status():
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    try:
        response = requests.get(f"{UBIDOTS_URL}switch/lv", headers=headers)  # Pastikan ada variabel switch di Ubidots
        if response.status_code == 200:
            return int(float(response.text))
    except Exception as e:
        print("Gagal mengambil status Switch dari Ubidots:", e)
    return 1  # Default 1 (mesin tetap hidup)

# === FUNGSI KIRIM DATA KE UBIDOTS ===
def send_to_ubidots(temp, hum, led_state, button_state):
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    data = {
        "temperature": round(temp, 2),
        "humidity": round(hum, 2),
        "led_status": led_state,
        "switch": button_state
    }
    try:
        response = requests.post(UBIDOTS_URL, json=data, headers=headers)
        print("Data terkirim ke Ubidots:", response.text)
    except Exception as e:
        print("Gagal mengirim ke Ubidots:", e)

# === FUNGSI KIRIM DATA KE FLASK DATABASE (MongoDB) ===
def send_to_flask(temp, hum, led_state, button_state):
    headers = {"Content-Type": "application/json"}
    data = {
        "temperature": round(temp, 2),
        "humidity": round(hum, 2),
        "led_status": led_state,
        "switch": button_state
    }
    try:
        response = requests.post(FLASK_SERVER_URL, json=data, headers=headers)
        print("Data terkirim ke Flask Database:", response.text)
    except Exception as e:
        print("Gagal mengirim ke Flask Database:", e)

# === LOOP UTAMA ===
led_state = 0  # Status awal LED

while True:
    try:
        # Cek status switch dari Ubidots
        switch_status = get_switch_status()
        if switch_status == 0:
            print("🔴 Mesin dimatikan oleh Ubidots! ESP32 akan restart dalam 5 detik...")
            time.sleep(5)
            machine.reset()  # Restart ESP32 agar bisa nyala lagi jika switch diubah ke 1

        time.sleep(2)
        dht_sensor.measure()
        temp = dht_sensor.temperature() / 23.4
        hum = dht_sensor.humidity() / 23.4

        # Baca tombol
        button_state = button.value()
        if button_state == 0:
            led_state = 1
        else:
            ubidots_led_status = get_led_status()
            if ubidots_led_status is not None:
                led_state = ubidots_led_status

        led.value(led_state)

        # Debugging
        print("\n===== DATA SENSOR =====")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {hum}%")
        print(f"LED Status: {'ON' if led_state else 'OFF'}")
        print(f"Switch Status: {switch_status}")
        print("========================\n")

        # Kirim data ke Ubidots
        send_to_ubidots(temp, hum, led_state, switch_status)

        # Kirim data ke Flask (MongoDB)
        send_to_flask(temp, hum, led_state, switch_status)

    except Exception as e:
        print("Error:", e)

    time.sleep(1)

