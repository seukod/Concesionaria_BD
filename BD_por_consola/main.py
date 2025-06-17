import os

def menu_modificaciones():
    while True:
        print("\n--- Menú de Modificaciones ---")
        print("1. Modificar compras (por implementar)")
        print("2. Modificar ventas (por implementar)")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("Funcionalidad para modificar compras aún no implementada.")
        elif opcion == "2":
            print("Funcionalidad para modificar ventas aún no implementada.")
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