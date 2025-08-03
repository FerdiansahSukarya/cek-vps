import pymysql
from supabase import create_client, Client
from datetime import datetime
import time

# Konfigurasi MySQL
try:
    mysql_conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="sensor_db"
    )
    print("? Terhubung ke MySQL")
except Exception as e:
    print(f"? Gagal koneksi MySQL: {e}")
    exit()

# Konfigurasi Supabase
SUPABASE_URL = "https://siosiigonlauesjlafbq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpb3NpaWdvbmxhdWVzamxhZmJxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTQ3ODUyMCwiZXhwIjoyMDY1MDU0NTIwfQ.7zdvu5Ltjr7J2SrHa4WmfFfxphmGxtTwHezvz1lEJpc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fungsi ambil data dari MySQL
def get_mysql_data(table):
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"? Gagal ambil data dari MySQL tabel '{table}': {e}")
        return []

# Fungsi ambil data dari Supabase
def get_supabase_data(table):
    try:
        response = supabase.table(table).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"? Gagal ambil data dari Supabase tabel '{table}': {e}")
        return []

# Fungsi update Supabase dari MySQL
def sync_mysql_to_supabase(table):
    local_data = get_mysql_data(table)
    remote_data = get_supabase_data(table)
    remote_ids = {row['id'] for row in remote_data}

    for row in local_data:
        if row['id'] not in remote_ids:
            # Konversi semua nilai datetime menjadi string
            clean_row = {}
            for k, v in row.items():
                if isinstance(v, datetime):
                    clean_row[k] = v.isoformat()
                else:
                    clean_row[k] = v

            print(f"? Menambahkan ke Supabase ({table}): {clean_row}")
            try:
                response = supabase.table(table).insert(clean_row).execute()
                print(f"? Hasil insert: {response}")
            except Exception as e:
                print(f"? Error saat insert ke Supabase: {e}")


# Jalankan sinkronisasi
tables = ["sensor_data", "tindakan", "evaluasi_tinggi"]

for table in tables:
    print(f"\n?? Sinkronisasi {table} dimulai...")
    sync_mysql_to_supabase(table)
    print(f"? Sinkronisasi {table} selesai.\n")
