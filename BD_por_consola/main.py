import os
from config import *
from autos import *
from ventas import *
from etl import run_etl  # <-- Añade esta línea

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')


def opcion_modificacion(tabla):
    while True:
        print(f"\n--- Opción de modificación en tabla {tabla} ---")
        print("1. Crear fila")
        print("2. Leer datos")
        print("3. Actualizar fila")
        print("4. Eliminar fila")
        print("5. Volver al menú de modificaciones")
        
        opcion = input("Seleccione una opción: ")
        limpiar_consola()
        if tabla == "autos":  
            if opcion == "1":
                
                crear_auto()
            elif opcion == "2":
                
                leer_autos()
            elif opcion == "3":
            
                actualizar_auto()
            elif opcion == "4":
                eliminar_auto()
            elif opcion == "5":
                return
            
            else:
                print("Opción no válida. Intente de nuevo.")
        elif tabla == "ventas":
            if opcion == "1":
                crear_venta()
            elif opcion == "2":
                leer_ventas()
            elif opcion == "3":
                actualizar_venta()
            elif opcion == "4":
                eliminar_venta()
            elif opcion == "5":
                return
            else:
                print("Opción no válida. Intente de nuevo.")
    
def menu_modificaciones():
    while True: 
        limpiar_consola()
        print("\n--- Menú de Modificaciones ---")
        print("1. Modificar tabla Autos")
        print("2. Modificar tabla de Ventas")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ") 
        if opcion == "1":
            limpiar_consola()
            opcion_modificacion("autos")
        elif opcion == "2":
            limpiar_consola()
            opcion_modificacion("ventas")
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def rellenar_base_datos():
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'ingresar_datos_tra.sql')
    sql_path = os.path.abspath(sql_path)
    print(f"Ejecutando script SQL: {sql_path}")
    import psycopg2
    from config import DB_CONFIG

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("Base de datos rellenada exitosamente.")
    except Exception as e:
        print("Error al ejecutar el script SQL:", e)

def main():
    create_database_if_not_exists()
    run_schema_scripts()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Modificaciones (compras/ventas)")
        print("2. Rellenar base de datos transaccional")
        print("3. Ejecutar ETL")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        limpiar_consola() 
        if opcion == "1":
            menu_modificaciones()
            limpiar_consola()
        elif opcion == "2":
            rellenar_base_datos()
        elif opcion == "3":
            run_etl()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()