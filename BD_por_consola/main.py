import os
# HAY QUE ELEGIR DOS TABLAS A MODIFICAR Y HACER QUE EL USUARIO PUEDA ELEGIR ENTRE ELLAS
# TAMBIÉN HAY QUE HACER QUE EL USUARIO ELIJA ENTRE CUALQUIER OPCION CRUD DE LAS TABLAS
# POR LO TANTO ESTA FUNCION HAY QUE MODIFICARLA

def opcion_modificacion(): #qué opcion del CRUD
    while True:
        print("\n--- Opción de modificación ---")
        print("1. Crear fila")
        print("2. Leer datos")
        print("3. Actualizar tabla")
        print("4. Eliminar fila")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            break
        elif opcion == "2":
            break
        elif opcion == "3":
            break
        elif opcion == "4":
            break
        elif opcion == "5":
            menu_modificaciones()

def menu_modificaciones():
    while True: 
        print("\n--- Menú de Modificaciones ---")
        print("1. Modificar tabla Autos (por implementar)")
        print("2. Modificar tabla de Ventas (por implementar)")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            opcion_modificacion()
        elif opcion == "2":
            opcion_modificacion()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def rellenar_base_datos():
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'agregar_datos.sql')
    sql_path = os.path.abspath(sql_path)
    print(f"Ejecutando script SQL: {sql_path}")
    import psycopg2
    from .config import DB_CONFIG

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
    while True:
        print("\n--- Menú Principal ---")
        print("1. Modificaciones (compras/ventas)")
        print("2. Rellenar base de datos transaccional")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_modificaciones()
        elif opcion == "2":
            rellenar_base_datos()
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()