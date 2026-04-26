import sys
import os
sys.path.append(os.path.join(os.getcwd(), "db_scripts"))
from db_utils import DB_CONFIG
import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connection successful")
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Database version: {db_version}")
        
        # List tables in public schema
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        print(f"Tables in public schema: {[t[0] for t in tables]}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
