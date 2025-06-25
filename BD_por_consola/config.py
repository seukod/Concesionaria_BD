import os
import psycopg2
import sys

def iniciar_usuario():
    import getpass

    user = input("Ingrese el nombre de usuario de PostgreSQL: ")
    if not user:
        user = "postgres"
        print("Usuario postgres por defecto.")
    password = getpass.getpass("Ingrese la contraseña de PostgreSQL: ")
    return user, password

user, password = iniciar_usuario()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": user,
    "password": password
}

def create_database_if_not_exists():
    tmp_config = DB_CONFIG.copy()
    tmp_config["database"] = "postgres"
    try:
        conn = psycopg2.connect(**tmp_config)
    except psycopg2.OperationalError as e:
        if 'password authentication failed' in str(e):
            print("Error: contraseña incorrecta. El programa se cerrará.")
            sys.exit(1)
        else:
            print("Error de conexión:", e)
            sys.exit(1)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'db_transac'")
    exists = cur.fetchone()
    if not exists:
        cur.execute("CREATE DATABASE db_transac")
        print("Base de datos 'db_transac' creada.")
    else:
        print("La base de datos 'db_transac' ya existe.")
    cur.close()
    conn.close()

def run_schema_scripts():
    import psycopg2
    # Ejecuta el script de transaccional
    tra_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ingresar_tabla_tra.sql'))
    with open(tra_path, 'r', encoding='utf-8') as f:
        sql_tra = f.read()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql_tra)
    conn.commit()
    print("Esquema 'transaccional' creado o actualizado.")
    cur.close()
    conn.close()

    # Ejecuta el script de analisis
    ana_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modificartablas.sql'))
    with open(ana_path, 'r', encoding='utf-8') as f:
        sql_ana = f.read()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql_ana)
    conn.commit()
    print("Esquema 'analisis' creado o actualizado.")
    cur.close()
    conn.close()

def tabla_existe(nombre_tabla):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT to_regclass(%s)", (nombre_tabla,))
    existe = cur.fetchone()[0] is not None
    cur.close()
    conn.close()
    return existe

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
    # Cambia aquí: agrega el esquema transaccional
    query = f'SELECT * FROM transaccional.{table}'
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