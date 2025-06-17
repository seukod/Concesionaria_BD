import os
from db_utils import create_row, read_rows, update_row, delete_row

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

def opcion_modificacion(tabla):
    while True:
        print(f"\n--- Opción de modificación en tabla {tabla} ---")
        print("1. Crear fila")
        print("2. Leer datos")
        print("3. Actualizar fila")
        print("4. Eliminar fila")
        print("5. Volver al menú de modificaciones")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print(f"Funcionalidad para crear fila en {tabla} (por implementar)")
            crear_auto()
        elif opcion == "2":
            print(f"Funcionalidad para leer datos de {tabla} (por implementar)")
            leer_autos()
        elif opcion == "3":
            print(f"Funcionalidad para actualizar fila en {tabla} (por implementar)")
            actualizar_auto()
        elif opcion == "4":
            print(f"Funcionalidad para eliminar fila en {tabla} (por implementar)")
            eliminar_auto()
        elif opcion == "5":
            menu_modificaciones()
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_modificaciones():
    while True: 
        print("\n--- Menú de Modificaciones ---")
        print("1. Modificar tabla Autos")
        print("2. Modificar tabla de Ventas")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            opcion_modificacion("autos")
        elif opcion == "2":
            opcion_modificacion("ventas")
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