# sensor_reader.py

import serial
import threading
import smbus2 as smbus
import time
import pymysql
from datetime import datetime
from supabase import create_client, Client

# === Konfigurasi Serial & I2C ===
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
bus = smbus.SMBus(1)
address = 0x04

# === Koneksi MySQL ===
mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="sensor_db"
)

# === Koneksi Supabase ===
SUPABASE_URL = "https://siosiigonlauesjlafbq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpb3NpaWdvbmxhdWVzamxhZmJxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTQ3ODUyMCwiZXhwIjoyMDY1MDU0NTIwfQ.7zdvu5Ltjr7J2SrHa4WmfFfxphmGxtTwHezvz1lEJpc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Data Shared ===
data_tinggi = 0.0
data_ph = 0.0
lock = threading.Lock()

def baca_serial():
    global data_tinggi
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("TINGGI:"):
                try:
                    tinggi = float(line.split(":")[1])
                    with lock:
                        data_tinggi = tinggi
                except ValueError:
                    pass

def baca_ph():
    global data_ph
    while True:
        try:
            data = bus.read_i2c_block_data(address, 0, 6)
            ph_raw = (data[4] << 8) | data[5]
            ph_value = ph_raw / 100.0
            with lock:
                data_ph = ph_value
        except OSError as e:
            print("I2C Error:", str(e))
        time.sleep(5)

def simpan_ke_mysql(ph, tinggi):
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sensor_data (waktu, ph, tinggi_cm) VALUES (%s, %s, %s)",
                (datetime.now(), ph, tinggi)
            )
        mysql_conn.commit()
    except Exception as e:
        print(f"Gagal simpan ke MySQL: {e}")

def get_mysql_data(table):
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"?? Gagal ambil data dari MySQL '{table}': {e}")
        return []

def get_supabase_data(table):
    try:
        response = supabase.table(table).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"?? Gagal ambil data Supabase '{table}': {e}")
        return []

def sync_mysql_to_supabase(table):
    local_data = get_mysql_data(table)
    remote_data = get_supabase_data(table)
    remote_ids = {row['id'] for row in remote_data}

    for row in local_data:
        if row['id'] not in remote_ids:
            clean_row = {
                k: v.isoformat() if isinstance(v, datetime) else v
                for k, v in row.items()
            }
            try:
                supabase.table(table).insert(clean_row).execute()
                print(f"? Sync ke Supabase ({table}): {clean_row}")
            except Exception as e:
                print(f"? Error insert ke Supabase: {e}")

def loop_simpan_dan_sync():
    while True:
        with lock:
            ph = data_ph
            tinggi = data_tinggi
        simpan_ke_mysql(ph, tinggi)

        for tbl in ["sensor_data", "tindakan", "evaluasi_tinggi"]:
            sync_mysql_to_supabase(tbl)

        time.sleep(30)  # setiap 10 detik

# Jalankan semua
if __name__ == "__main__":
    threading.Thread(target=baca_serial, daemon=True).start()
    threading.Thread(target=baca_ph, daemon=True).start()
    loop_simpan_dan_sync()
