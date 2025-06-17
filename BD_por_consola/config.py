import psycopg2
from .config import DB_CONFIG

DB_CONFIG = {
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": 5432,
    "database": "tabladehechos",
    "user": "postgres.qdxsvygmfuqrrcaisqvw",
    "password": "0NzSHHo6Ee9Hl4BI"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_row(table, columns, values):
    conn = get_connection()
    cur = conn.cursor()
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()

def read_rows(table):
    conn = get_connection()
    cur = conn.cursor()
    query = f"SELECT * FROM {table}"
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def update_row(table, id_column, id_value, update_columns, update_values):
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ', '.join([f"{col} = %s" for col in update_columns])
    query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
    cur.execute(query, update_values + [id_value])
    conn.commit()
    cur.close()
    conn.close()

def delete_row(table, id_column, id_value):
    conn = get_connection()
    cur = conn.cursor()
    query = f"DELETE FROM {table} WHERE {id_column} = %s"
    cur.execute(query, [id_value])
    conn.commit()
    cur.close()
    conn.close()