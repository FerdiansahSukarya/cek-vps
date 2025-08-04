from flask import Flask, render_template, redirect, url_for, request
import pymysql
from datetime import datetime
from sensor_reader import data_ph, data_tinggi, lock, simpan_ke_mysql, start_background_threads

app = Flask(__name__)

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
        return render_template("index.html", row=row)
    except Exception as e:
        return f"Error: {e}"

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
