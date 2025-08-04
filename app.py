from flask import Flask, render_template, session, redirect, url_for, request
import pymysql, threading
from datetime import datetime
from sensor_reader import data_ph, data_tinggi, lock, simpan_ke_mysql, start_background_threads
#from relay_runner import run_relay_loop  # fungsi utama relay, nanti kita atur
from relay_runner import run_relay_loop, stop_relay_loop

app = Flask(__name__)
app.secret_key = 'ferdi123'  # ? Tambahkan baris ini
relay_running = False
relay_thread = None

# Jalankan sensor & penyimpanan di latar belakang
start_background_threads()

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="sensor_db",
        cursorclass=pymysql.cursors.Cursor
    )

@app.route("/")
def index():
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT waktu, ph, tinggi_cm FROM sensor_data ORDER BY waktu DESC LIMIT 1")
                row = cursor.fetchone()

            # Ambil log relay terbaru jika ada
            latest_log = None
            if relay_running:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT waktu, durasi, jenis 
                        FROM relay_log 
                        WHERE status='on' 
                        ORDER BY waktu DESC LIMIT 1
                    """)
                    latest_log = cursor.fetchone()

        return render_template("index.html", row=row, relay_running=relay_running, latest_log=latest_log)
    except Exception as e:
        return f"Error: {e}"


@app.route("/toggle", methods=["POST"])
def toggle():
    global relay_running, relay_thread

    if session.get("relay_running"):
        relay_running = False
        session["relay_running"] = False
    else:
        relay_running = True
        session["relay_running"] = True
        relay_thread = threading.Thread(target=run_relay_loop, daemon=True)
        relay_thread.start()

    return redirect("/")

@app.route("/riwayat")
def riwayat():
    try:
        page = int(request.args.get('page', 1))
        per_page = 25
        offset = (page - 1) * per_page

        conn = get_connection()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT waktu, ph, tinggi_cm FROM sensor_data ORDER BY waktu DESC LIMIT %s OFFSET %s", (per_page + 1, offset))
                rows = cursor.fetchall()

        has_more = len(rows) > per_page
        data = rows[:per_page]
        return render_template("riwayat.html", data=data, page=page, has_more=has_more, start_index=offset)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
