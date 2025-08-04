import time
import subprocess
from datetime import datetime
import requests
from db import get_connection

# Konstanta
DURASI = "20 detik"
PEMBERIAN_ULANG = "1 minggu"
SUPABASE_URL = "https://siosiigonlauesjlafbq.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpb3NpaWdvbmxhdWVzamxhZmJxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTQ3ODUyMCwiZXhwIjoyMDY1MDU0NTIwfQ.7zdvu5Ltjr7J2SrHa4WmfFfxphmGxtTwHezvz1lEJpc"

# STATUS KONTROL
running = False  # akan dikontrol dari app.py

def get_latest_ph():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ph FROM sensor_data ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None
    except Exception as e:
        print("[!] Gagal mengambil pH:", e)
        return None

def send_to_supabase(ph, waktu, jenis, status):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "ph": ph,
        "waktu": waktu,
        "durasi": DURASI,
        "pemberian_ulang": PEMBERIAN_ULANG,
        "jenis": jenis,
        "status": status
    }
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/relay_log", json=data, headers=headers)
        print("? Supabase:", r.status_code)
    except Exception as e:
        print("[!] Supabase error:", e)

def log_relay(ph, waktu, jenis, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO relay_log (ph, waktu, durasi, pemberian_ulang, jenis, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ph, waktu, DURASI, PEMBERIAN_ULANG, jenis, status))
        conn.commit()
        cursor.close()
        conn.close()
        send_to_supabase(ph, waktu, jenis, status)
    except Exception as e:
        print("[!] Gagal log:", e)

def run_relay_loop():
    global running
    running = True
    while running:
        ph = get_latest_ph()
        if ph is None:
            print("[-] Tidak ada data pH.")
            break

        jenis = "n1" if ph < 5.0 else "n2"
        script = "a.py" if jenis == "n1" else "b.py"
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            subprocess.run(["python3", script])
            log_relay(ph, waktu, jenis, "on")
            print(f"[{waktu}] Relay {jenis} ON (pH={ph})")
            time.sleep(20)
            log_relay(ph, waktu, jenis, "off")
            print(f"[{waktu}] Relay {jenis} OFF")
        except Exception as e:
            print("[!] Gagal menyalakan relay:", e)

        print("? Tunggu 1 minggu...")
        for i in range(7 * 24 * 60):  # setiap menit
            if not running:
                print("[X] Dihentikan oleh pengguna.")
                return
            time.sleep(60)

def stop_relay_loop():
    global running
    running = False
