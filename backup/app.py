from flask import Flask, render_template, request, redirect, url_for
import serial
import threading
import smbus2 as smbus
import time

# === Konfigurasi Serial untuk Arduino ===
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

# === Konfigurasi I2C untuk pH ===
bus = smbus.SMBus(1)
address = 0x04

# === Inisialisasi Flask ===
app = Flask(__name__)

# === Data bersama ===
data_tinggi = {"nilai": 0.0}
data_ph = {"nilai": 0.0}
lock = threading.Lock()

# === Fungsi pembacaan Serial dari Arduino (tinggi air) ===
def baca_serial():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("TINGGI:"):
                try:
                    tinggi = float(line.split(":")[1])
                    with lock:
                        data_tinggi["nilai"] = tinggi
                except ValueError:
                    pass

# === Fungsi pembacaan pH via I2C ===
def baca_ph():
    while True:
        try:
            data = bus.read_i2c_block_data(address, 0, 6)
            ph_raw = (data[4] << 8) | data[5]
            ph_value = ph_raw / 100.0
            with lock:
                data_ph["nilai"] = ph_value
        except OSError as e:
            print("I2C Error:", str(e))
        time.sleep(5)

# === Jalankan thread untuk pembacaan data ===
threading.Thread(target=baca_serial, daemon=True).start()
threading.Thread(target=baca_ph, daemon=True).start()

# === Route utama ===
@app.route('/')
def index():
    with lock:
        tinggi = data_tinggi["nilai"]
        ph = data_ph["nilai"]
    return render_template("index.html", tinggi=tinggi, ph=ph)

# === Route untuk kontrol relay ===
@app.route('/relay/<int:nomor>/<status>')
def relay(nomor, status):
    if nomor in [1, 2] and status in ["on", "off"]:
        perintah = f"RELAY{nomor}_{status.upper()}\n"
        ser.write(perintah.encode())
    return redirect(url_for('index'))

# === Run aplikasi ===
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
