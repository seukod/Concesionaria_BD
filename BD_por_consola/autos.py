from config import *
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_auto():
    limpiar_consola()
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    anio = input("Año: ")
    create_row("autos", ["marca", "modelo", "anio"], [marca, modelo, anio])
    print("Auto creado.")
    input("\nPresione Enter para continuar...")  

def leer_autos():
    limpiar_consola()
    colnames, rows = read_rows("autos")
    print(colnames)
    for row in rows:
        print(row)
    input("\nPresione Enter para continuar...")

def actualizar_auto():
    limpiar_consola()
    id_auto = input("ID del auto a actualizar: ")
    campo = input("Campo a actualizar (marca/modelo/anio): ")
    valor = input(f"Nuevo valor para {campo}: ")
    update_row("autos", "id", id_auto, [campo], [valor])
    print("Auto actualizado.")
    input("\nPresione Enter para continuar...")

def eliminar_auto():
    limpiar_consola()
    id_auto = input("ID del auto a eliminar: ")
    delete_row("autos", "id", id_auto)
    print("Auto eliminado.")
    input("\nPresione Enter para continuar...")
