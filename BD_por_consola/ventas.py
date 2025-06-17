from config import *

def crear_venta():
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

def leer_ventas():
    colnames, rows = read_rows("ventas")
    print(colnames)
    for row in rows:
        print(row)

def actualizar_venta():
    id_venta = input("ID de la venta a actualizar: ")
    campo = input("Campo a actualizar (id_concesionaria/id_usuario/id_auto/monto/fecha_venta): ")
    valor = input(f"Nuevo valor para {campo}: ")
    update_row("ventas", "id_venta", id_venta, [campo], [valor])
    print("Venta actualizada.")

def eliminar_venta():
    id_venta = input("ID de la venta a eliminar: ")
    delete_row("ventas", "id_venta", id_venta)
    print("Venta eliminada.")