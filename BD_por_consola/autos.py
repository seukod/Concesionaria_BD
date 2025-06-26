from config import *
import psycopg2
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_row(table, columns, values):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cols = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en create_row: {e}")
        raise

def update_row(table, key_column, key_value, columns, values):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        set_clause = ', '.join([f"{col} = %s" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {key_column} = %s"
        cur.execute(query, values + [key_value])
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en update_row: {e}")
        raise

def delete_row(table, key_column, key_value):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = f"DELETE FROM {table} WHERE {key_column} = %s"
        cur.execute(query, (key_value,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en delete_row: {e}")
        raise

def read_rows(table):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return colnames, rows
    except Exception as e:
        print(f"Error en read_rows: {e}")
        raise

def crear_auto():
    limpiar_consola()
    try:
        patente = input("Ingrese patente (6 caracteres, letras en mayúscula): ")
        precio = input("Ingrese precio: ")
        auto_prueba = input("¿Es auto de prueba? (True/False): ")
        disponible = input("¿Está disponible? (True/False): ")
        fecha_llegada = input("Fecha de ingreso (YYYY-MM-DD): ")
        kilometraje = input("Kilometraje: ")
        modelo = input("Modelo (ID): ")
        
        create_row(
            "autos", 
            ["patente", "precio", "auto_prueba", "disponible", "fecha_llegada", "kilometraje", "modelo"],
            [patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, modelo]
        )
        print("Auto creado.")
    except Exception as e:
        print(f"Error al crear el auto: {e}")
    input("\nPresione Enter para continuar...")  

def leer_autos():
    limpiar_consola()
    try:
        colnames, rows = read_rows("autos")
        print(colnames)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error al leer los autos: {e}")
    input("\nPresione Enter para continuar...")

def actualizar_auto():
    limpiar_consola()
    try:
        patente = input("Patente (PK) del auto a actualizar: ")
        campo = input("Campo a actualizar (precio/auto_prueba/disponible/fecha_llegada/kilometraje/modelo): ")
        valor = input(f"Nuevo valor para {campo}: ")
        update_row("autos", "patente", patente, [campo], [valor])
        print("Auto actualizado.")
    except Exception as e:
        print(f"Error al actualizar el auto: {e}")
    input("\nPresione Enter para continuar...")

def eliminar_auto():
    limpiar_consola()
    try:
        patente = input("Patente del auto a marcar como no disponible: ")
        update_row("autos", "patente", patente, ["disponible"], ["False"])
        print("Auto marcado como no disponible.")
    except Exception as e:
        print(f"Error al eliminar el estado del auto: {e}")
    input("\nPresione Enter para continuar...")
