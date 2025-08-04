import RPi.GPIO as GPIO
import time
import datetime
from db import get_connection

RELAY_PIN = 17
DURASI = 20  # detik

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    # Aktifkan relay (tergantung logika LOW/HIGH, sesuaikan)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(DURASI)
    GPIO.output(RELAY_PIN, GPIO.HIGH)

    # Log ke database
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    deskripsi = "POC otomatis via N1 (a.py)"
    cursor.execute("INSERT INTO tindakan (waktu_tindakan, jenis, durasi_detik, deskripsi) VALUES (%s, %s, %s, %s)",
                   (now, "N1", DURASI, deskripsi))
    conn.commit()
    conn.close()

    print("Relay aktif dan tindakan tercatat.")
except Exception as e:
    print("Terjadi kesalahan:", e)
finally:
    GPIO.cleanup()
