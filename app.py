from flask import Flask, render_template, redirect, url_for
import pymysql
from datetime import datetime

app = Flask(__name__)

# === Koneksi ke MySQL ===
mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="sensor_db"
)

@app.route("/")
def index():
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT waktu, ph, tinggi_cm FROM sensor_data ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
        return render_template("index.html", row=row)
    except Exception as e:
        return f"Error: {e}"

@app.route("/relay/<int:nomor>/<status>")
def kontrol_relay(nomor, status):
    if nomor in [1, 2] and status in ["on", "off"]:
        jenis = f"relay{nomor}"
        durasi = 0  # atau bisa ditentukan sesuai kebutuhan
        deskripsi = f"User menyalakan {jenis} ke {status.upper()}"
        waktu = datetime.now()

        with mysql_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tindakan (waktu_tindakan, jenis, durasi_detik, deskripsi, status)
                VALUES (%s, %s, %s, %s, 'pending')
            """, (waktu, jenis, durasi, deskripsi))
            mysql_conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
