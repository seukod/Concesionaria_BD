import psycopg2
from .config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()