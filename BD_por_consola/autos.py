from config import *

def crear_auto():
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    anio = input("Año: ")
    create_row("autos", ["marca", "modelo", "anio"], [marca, modelo, anio])
    print("Auto creado.")

def leer_autos():
    colnames, rows = read_rows("autos")
    print(colnames)
    for row in rows:
        print(row)

def actualizar_auto():
    id_auto = input("ID del auto a actualizar: ")
    campo = input("Campo a actualizar (marca/modelo/anio): ")
    valor = input(f"Nuevo valor para {campo}: ")
    update_row("autos", "id", id_auto, [campo], [valor])
    print("Auto actualizado.")

def eliminar_auto():
    id_auto = input("ID del auto a eliminar: ")
    delete_row("autos", "id", id_auto)
    print("Auto eliminado.")
