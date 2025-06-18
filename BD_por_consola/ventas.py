from config import *
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_venta():
    limpiar_consola()
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
    input("\nPresione Enter para continuar...")

def leer_ventas():
    limpiar_consola()
    colnames, rows = read_rows("ventas")
    print(colnames)
    for row in rows:
        print(row)
    input("\nPresione Enter para continuar...")

def actualizar_venta():
    limpiar_consola()
    id_venta = input("ID de la venta a actualizar: ")
    campo = input("Campo a actualizar (id_concesionaria/id_usuario/id_auto/monto/fecha_venta): ")
    valor = input(f"Nuevo valor para {campo}: ")
    update_row("ventas", "id_venta", id_venta, [campo], [valor])
    print("Venta actualizada.")
    input("\nPresione Enter para continuar...")

def eliminar_venta():
    limpiar_consola()
    id_venta = input("ID de la venta a eliminar: ")
    delete_row("ventas", "id_venta", id_venta)
    print("Venta eliminada.")
    input("\nPresione Enter para continuar...")
