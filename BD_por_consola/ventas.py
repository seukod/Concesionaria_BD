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

def crear_venta():
    limpiar_consola()
    try:
        id_concesionaria = input("ID concesionaria: ")
        id_usuario = input("RUT usuario: ")
        id_auto = input("Patente auto: ")
        monto = input("Monto: ")
        fecha_venta = input("Fecha de venta (YYYY-MM-DD HH:MM:SS): ")
        create_row(
            "ventas",
            ["id_concesionaria", "id_usuario", "id_auto", "monto", "fecha_venta"],
            [id_concesionaria, id_usuario, id_auto, monto, fecha_venta]
        )
        print("Venta creada.")
    except Exception as e:
        print(f"Error al crear la venta: {e}")
    input("\nPresione Enter para continuar...")

def leer_ventas():
    limpiar_consola()
    try:
        colnames, rows = read_rows("ventas")
        print(colnames)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error al leer las ventas: {e}")
    input("\nPresione Enter para continuar...")

def actualizar_venta():
    limpiar_consola()
    try:
        id_venta = input("ID de la venta a actualizar: ")
        campo = input("Campo a actualizar (id_concesionaria/id_usuario/id_auto/monto/fecha_venta): ")
        valor = input(f"Nuevo valor para {campo}: ")
        update_row("ventas", "id_venta", id_venta, [campo], [valor])
        print("Venta actualizada.")
    except Exception as e:
        print(f"Error al actualizar la venta: {e}")
    input("\nPresione Enter para continuar...")

def eliminar_venta():
    limpiar_consola()
    try:
        id_venta = input("ID de la venta a eliminar: ")
        delete_row("ventas", "id_venta", id_venta)
        print("Venta eliminada.")
    except Exception as e:
        print(f"Error al eliminar la venta: {e}")
    input("\nPresione Enter para continuar...")

