from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta
from db import get_connection
import subprocess

app = Flask(__name__)
app.secret_key = 'rahasia'  # untuk flash messages

DURASI = "20 detik"
PEMBERIAN_ULANG = "1 minggu"

def get_latest_ph():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ph FROM sensor_data ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(result[0]) if result else None

def get_last_activation_time(jenis):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT waktu FROM relay_log 
        WHERE jenis = %s AND status = 'on' 
        ORDER BY id DESC LIMIT 1
    """, (jenis,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def log_relay(ph, waktu, jenis, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO relay_log (ph, waktu, durasi, pemberian_ulang, jenis, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ph, waktu, DURASI, PEMBERIAN_ULANG, jenis, status))
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/relay", methods=["GET", "POST"])
def relay_control():
    ph = get_latest_ph()
    if ph is None:
        flash("Data pH tidak tersedia.")
        return render_template("relay.html", status="Tidak ada data")

    jenis = "n1" if ph < 5.9 else "n2"
    script_path = "a.py" if jenis == "n1" else "b.py"
    waktu_now = datetime.now()
    waktu_str = waktu_now.strftime("%H:%M")

    last_activation = get_last_activation_time(jenis)
    allow_activation = False

    if last_activation is None:
        allow_activation = True
    else:
        delta = datetime.now() - last_activation
        if delta >= timedelta(weeks=1):
            allow_activation = True

    if request.method == "POST":
        if allow_activation:
            subprocess.run(["python3", script_path])
            log_relay(ph, waktu_str, jenis, "on")
            flash(f"Relay {jenis.upper()} aktif karena pH = {ph}")
        else:
            flash(f"Relay {jenis.upper()} sudah aktif minggu ini. Tunggu hingga minggu depan.")
        return redirect("/relay")

    return render_template("relay.html", ph=ph, jenis=jenis, allow=allow_activation)

if __name__ == "__main__":
    app.run(debug=True)
