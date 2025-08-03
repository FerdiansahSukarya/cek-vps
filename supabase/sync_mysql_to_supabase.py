import pymysql
from supabase import create_client, Client
from datetime import datetime
import time

# === Konfigurasi MySQL Lokal ===
mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",  # Ganti jika ada password
    database="sensor_db"
)

# === Konfigurasi Supabase ===
SUPABASE_URL = "https://siosiigonlauesjlafbq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpb3NpaWdvbmxhdWVzamxhZmJxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTQ3ODUyMCwiZXhwIjoyMDY1MDU0NTIwfQ.7zdvu5Ltjr7J2SrHa4WmfFfxphmGxtTwHezvz1lEJpc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Fungsi Ambil Data dari MySQL ===
def get_mysql_data(table):
    with mysql_conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# === Fungsi Ambil Data dari Supabase ===
def get_supabase_data(table):
    return supabase.table(table).select("*").execute().data

# === Fungsi Sinkronisasi MySQL ? Supabase ===
def sync_mysql_to_supabase(table):
    local_data = get_mysql_data(table)
    remote_data = get_supabase_data(table)
    remote_ids = {row['id'] for row in remote_data}

    for row in local_data:
        if row['id'] not in remote_ids:
            supabase.table(table).insert(row).execute()

# === Fungsi Sinkronisasi Supabase ? MySQL ===
def sync_supabase_to_mysql(table):
    local_data = get_mysql_data(table)
    local_ids = {row['id'] for row in local_data}
    remote_data = get_supabase_data(table)

    with mysql_conn.cursor() as cursor:
        for row in remote_data:
            if row['id'] not in local_ids:
                keys = ", ".join(row.keys())
                values = ", ".join(["%s"] * len(row))
                sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"
                cursor.execute(sql, list(row.values()))
        mysql_conn.commit()

# === Daftar Tabel yang Akan Disinkronkan ===
tables = ["sensor_data", "tindakan", "evaluasi_tinggi"]

# === Proses Sinkronisasi Dua Arah ===
for table in tables:
    sync_mysql_to_supabase(table)
    sync_supabase_to_mysql(table)

print("Sinkronisasi selesai.")
