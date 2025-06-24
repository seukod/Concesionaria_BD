from config import *
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_auto():
    limpiar_consola()
    try:
        patente = input("Ingrece patente (son 6 carcteres y las letras en mayuscula): ")
        precio = input("Ingrese precio: ")
        auto_prueba = input("Ingrese auto prueba (True/False): ")
        disponible = input("¿Está disponible? (True/False): ")
        fecha_llegada = input("Fecha de ingreso (dd/mm/yyyy): ")
        kilometraje = input("Kilometraje: ")
        modelo = input("Modelo: ")
        
        create_row("autos", ["patente","precio","auto_prueba","disponible","fecha_llegada","kilometraje", "modelo"],
                    [patente, precio, auto_prueba,disponible,fecha_llegada,kilometraje, modelo])
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
        id_auto = input("ID del auto a actualizar: ")
        campo = input("Campo a actualizar (marca/modelo/anio): ")
        valor = input(f"Nuevo valor para {campo}: ")
        update_row("autos", "id", id_auto, [campo], [valor])
        print("Auto actualizado.")
    except Exception as e:
        print(f"Error al actualizar el auto: {e}")
    input("\nPresione Enter para continuar...")

def eliminar_auto():
    limpiar_consola()
    try:
        id_auto = input("ID del auto a eliminar: ")
        delete_row("autos", "id", id_auto)
        print("Auto eliminado.")
    except Exception as e:
        print(f"Error al eliminar el auto: {e}")
    input("\nPresione Enter para continuar...")
