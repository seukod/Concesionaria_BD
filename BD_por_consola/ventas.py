"""
Módulo para operaciones CRUD específicas de la tabla ventas.
Utiliza el módulo crud_utils para operaciones genéricas de base de datos.
"""

from crud_utils import *
from config import DB_CONFIG
from datetime import datetime

def crear_venta():
    """Crea una nueva venta en la base de datos"""
    limpiar_consola()
    try:
        print("=== Crear Nueva Venta ===")
        
        # Mostrar concesionarias disponibles
        print("Concesionarias disponibles:")
        colnames, concesionarias = read_rows("concesionarias", ["id_concesionarias", "direccion"])
        if concesionarias:
            for conc in concesionarias:
                print(f"ID: {conc[0]}, Dirección: {conc[1]}")
        
        id_concesionaria = int(input("\nID concesionaria: "))
        
        # Mostrar usuarios disponibles
        print("\nUsuarios disponibles:")
        colnames, usuarios = read_rows("usuarios", ["rut", "nombre", "apellido"])
        if usuarios:
            for usuario in usuarios[:10]:  # Mostrar solo los primeros 10
                print(f"RUT: {usuario[0]}, Nombre: {usuario[1]} {usuario[2]}")
        
        id_usuario = int(input("\nRUT usuario: "))
        
        # Mostrar autos disponibles
        print("\nAutos disponibles:")
        colnames, autos = read_rows("autos", ["patente", "precio", "modelo"], 
                                   where_clause="disponible = true")
        if autos:
            for auto in autos:
                print(f"Patente: {auto[0]}, Precio: {auto[1]}, Modelo: {auto[2]}")
        
        id_auto = input("\nPatente auto: ").strip().upper()
        monto = float(input("Monto: "))
        
        # Usar fecha actual si no se especifica
        fecha_input = input("Fecha de venta (YYYY-MM-DD HH:MM:SS) [Enter para usar fecha actual]: ").strip()
        if not fecha_input:
            fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            fecha_venta = fecha_input
        
        success = create_row(
            "ventas",
            ["id_concesionaria", "id_usuario", "id_auto", "monto", "fecha_venta"],
            [id_concesionaria, id_usuario, id_auto, monto, fecha_venta]
        )
        
        if success:
            print("✓ Venta creada exitosamente.")
            # Marcar el auto como no disponible
            update_result = update_row("autos", "patente", id_auto, ["disponible"], [False])
            if update_result:
                print("✓ Auto marcado como vendido.")
        else:
            print("✗ Error al crear la venta.")
            
    except ValueError as e:
        print(f"Error: Valor inválido ingresado - {e}")
    except Exception as e:
        print(f"Error inesperado al crear la venta: {e}")
    
    input("\nPresione Enter para continuar...")

def leer_ventas():
    """Lee y muestra todas las ventas de la base de datos"""
    limpiar_consola()
    try:
        print("=== Lista de Ventas ===")
        
        # Consulta con JOIN para mostrar información más legible
        query = """
        SELECT 
            v.id_venta,
            v.id_concesionaria,
            c.direccion as direccion_concesionaria,
            v.id_usuario,
            u.nombre || ' ' || u.apellido as nombre_usuario,
            v.id_auto,
            v.monto,
            v.fecha_venta
        FROM transaccional.ventas v
        LEFT JOIN transaccional.concesionarias c ON v.id_concesionaria = c.id_concesionarias
        LEFT JOIN transaccional.usuarios u ON v.id_usuario = u.rut
        ORDER BY v.fecha_venta DESC
        """
        
        colnames, rows = execute_custom_query(query)
        
        if colnames is None or rows is None:
            print("Error al obtener los datos de ventas.")
            input("\nPresione Enter para continuar...")
            return
        
        if not rows:
            print("No hay ventas registradas en la base de datos.")
            input("\nPresione Enter para continuar...")
            return
        
        # Mostrar encabezados
        headers = ["ID", "ID_Conc", "Concesionaria", "RUT", "Cliente", "Patente", "Monto", "Fecha"]
        print("\n" + " | ".join(f"{h:<12}" for h in headers))
        print("-" * 120)
        
        # Mostrar datos
        for row in rows:
            formatted_row = [
                str(row[0])[:12],  # ID venta
                str(row[1])[:12],  # ID concesionaria
                str(row[2] or "N/A")[:12],  # Dirección concesionaria
                str(row[3])[:12],  # RUT usuario
                str(row[4] or "N/A")[:12],  # Nombre usuario
                str(row[5])[:12],  # Patente auto
                f"${row[6]:,.0f}"[:12],  # Monto
                str(row[7])[:12]   # Fecha
            ]
            print(" | ".join(f"{cell:<12}" for cell in formatted_row))
        
        print(f"\nTotal de ventas: {len(rows)}")
        
    except Exception as e:
        print(f"Error al leer las ventas: {e}")
    
    input("\nPresione Enter para continuar...")

def actualizar_venta():
    """Actualiza una venta existente en la base de datos"""
    limpiar_consola()
    try:
        print("=== Actualizar Venta ===")
        
        # Mostrar ventas disponibles
        print("Ventas disponibles:")
        colnames, rows = read_rows("ventas", ["id_venta", "id_auto", "monto", "fecha_venta"])
        
        if not rows:
            print("No hay ventas para actualizar.")
            input("\nPresione Enter para continuar...")
            return
        
        for row in rows:
            print(f"ID: {row[0]}, Auto: {row[1]}, Monto: ${row[2]:,.0f}, Fecha: {row[3]}")
        
        print("\n" + "="*50)
        id_venta = int(input("ID de la venta a actualizar: "))
        
        # Verificar que la venta existe
        colnames, existing = read_rows("ventas", where_clause="id_venta = %s", where_values=[id_venta])
        if not existing:
            print(f"No se encontró una venta con ID {id_venta}")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCampos disponibles para actualizar:")
        campos_disponibles = ["id_concesionaria", "id_usuario", "id_auto", "monto", "fecha_venta"]
        for i, campo in enumerate(campos_disponibles, 1):
            print(f"{i}. {campo}")
        
        opcion = input("\nSeleccione el número del campo a actualizar: ").strip()
        
        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(campos_disponibles):
                campo = campos_disponibles[indice]
                valor = input(f"Nuevo valor para {campo}: ").strip()
                
                # Convertir el valor según el tipo de campo
                if campo in ["id_concesionaria", "id_usuario"]:
                    valor = int(valor)
                elif campo == "monto":
                    valor = float(valor)
                elif campo == "id_auto":
                    valor = valor.upper()
                
                success = update_row("ventas", "id_venta", id_venta, [campo], [valor])
                
                if success:
                    print("✓ Venta actualizada exitosamente.")
                else:
                    print("✗ No se pudo actualizar la venta.")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            
    except Exception as e:
        print(f"Error al actualizar la venta: {e}")
    
    input("\nPresione Enter para continuar...")

def eliminar_venta():
    """Elimina una venta de la base de datos"""
    limpiar_consola()
    try:
        print("=== Eliminar Venta ===")
        
        # Mostrar ventas disponibles
        print("Ventas disponibles:")
        colnames, rows = read_rows("ventas", ["id_venta", "id_auto", "monto", "fecha_venta"])
        
        if not rows:
            print("No hay ventas para eliminar.")
            input("\nPresione Enter para continuar...")
            return
        
        for row in rows:
            print(f"ID: {row[0]}, Auto: {row[1]}, Monto: ${row[2]:,.0f}, Fecha: {row[3]}")
        
        print("\n" + "="*50)
        id_venta = int(input("ID de la venta a eliminar: "))
        
        # Obtener información de la venta antes de eliminarla
        colnames, venta_info = read_rows("ventas", where_clause="id_venta = %s", where_values=[id_venta])
        
        if not venta_info:
            print(f"No se encontró una venta con ID {id_venta}")
            input("\nPresione Enter para continuar...")
            return
        
        # Confirmar la eliminación
        auto_patente = venta_info[0][3]  # Asumiendo que id_auto está en la posición 3
        confirmar = input(f"¿Está seguro de eliminar la venta ID {id_venta}? (s/n): ").strip().lower()
        
        if confirmar == 's':
            success = delete_row("ventas", "id_venta", id_venta)
            
            if success:
                print("✓ Venta eliminada exitosamente.")
                # Marcar el auto como disponible nuevamente
                update_result = update_row("autos", "patente", auto_patente, ["disponible"], [True])
                if update_result:
                    print("✓ Auto marcado como disponible nuevamente.")
            else:
                print("✗ No se pudo eliminar la venta.")
        else:
            print("Operación cancelada.")
            
    except Exception as e:
        print(f"Error al eliminar la venta: {e}")
    
    input("\nPresione Enter para continuar...")

def buscar_ventas_por_usuario(rut_usuario):
    """
    Busca todas las ventas de un usuario específico.
    
    Args:
        rut_usuario (int): RUT del usuario
    
    Returns:
        list: Lista de ventas del usuario
    """
    try:
        colnames, rows = read_rows("ventas", where_clause="id_usuario = %s", where_values=[rut_usuario])
        
        if rows:
            return [dict(zip(colnames, row)) for row in rows]
        return []
    except Exception as e:
        print(f"Error al buscar ventas por usuario: {e}")
        return []

def obtener_estadisticas_ventas():
    """
    Obtiene estadísticas básicas de ventas.
    
    Returns:
        dict: Diccionario con estadísticas de ventas
    """
    try:
        # Total de ventas
        query_total = "SELECT COUNT(*), SUM(monto) FROM transaccional.ventas"
        colnames, result = execute_custom_query(query_total)
        
        if result:
            total_ventas = result[0][0]
            monto_total = result[0][1] or 0
            
            # Venta promedio
            promedio = monto_total / total_ventas if total_ventas > 0 else 0
            
            return {
                'total_ventas': total_ventas,
                'monto_total': monto_total,
                'venta_promedio': promedio
            }
        return None
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return None

