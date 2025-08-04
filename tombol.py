import time
import subprocess
from datetime import datetime
import requests
from db import get_connection  # asumsi koneksi ke MySQL


# Konstanta
DURASI = "20 detik"
PEMBERIAN_ULANG = "1 minggu"

# Supabase info
SUPABASE_URL = "https://siosiigonlauesjlafbq.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpb3NpaWdvbmxhdWVzamxhZmJxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTQ3ODUyMCwiZXhwIjoyMDY1MDU0NTIwfQ.7zdvu5Ltjr7J2SrHa4WmfFfxphmGxtTwHezvz1lEJpc"

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
        print("? Gagal mengambil data pH dari MySQL:", e)
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
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/relay_log",
            json=data,
            headers=headers
        )
        if response.status_code == 201:
            print("? Data dikirim ke Supabase.")
        else:
            print(f"?? Supabase gagal: {response.status_code} - {response.text}")
    except Exception as e:
        print("? Error kirim Supabase:", e)

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
        print("? Gagal log ke MySQL atau Supabase:", e)

def run_relay():
    ph = get_latest_ph()
    if ph is None:
        print("?? Data pH tidak tersedia. Melewati siklus ini.")
        return

    jenis = "n1" if ph < 5.9 else "n2"
    script_path = "a.py" if jenis == "n1" else "b.py"
    waktu_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        subprocess.run(["python3", script_path])
        log_relay(ph, waktu_now, jenis, "on")
        print(f"[{waktu_now}] Relay {jenis} ON (pH = {ph})")

        time.sleep(20)

        log_relay(ph, waktu_now, jenis, "off")
        print(f"[{waktu_now}] Relay {jenis} OFF setelah 20 detik")
    except Exception as e:
        print("? Error saat mengaktifkan relay:", e)

if __name__ == "__main__":
    while True:
        try:
            run_relay()
            print("? Menunggu 1 minggu untuk siklus berikutnya...\n")
            time.sleep(7 * 24 * 60 * 60)  # 1 minggu
        except KeyboardInterrupt:
            print("\n?? Program dihentikan manual.")
            break
        except Exception as e:
            print("?? Error tak terduga:", e)
            time.sleep(60)  # tunggu 1 menit dan coba lagi
