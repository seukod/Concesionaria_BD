from crud_utils import *
from config import DB_CONFIG

def crear_auto():
    """Crea un nuevo auto en la base de datos"""
    limpiar_consola()
    try:
        print("=== Crear Nuevo Auto ===")
        patente = input("Ingrese patente (6 caracteres, letras en mayúscula): ").strip().upper()
        
        # Validar patente
        if len(patente) != 6:
            print("Error: La patente debe tener exactamente 6 caracteres.")
            input("\nPresione Enter para continuar...")
            return
        
        precio = float(input("Ingrese precio: "))
        auto_prueba = input("¿Es auto de prueba? (True/False): ").strip().lower() == 'true'
        disponible = input("¿Está disponible? (True/False): ").strip().lower() == 'true'
        fecha_llegada = input("Fecha de ingreso (YYYY-MM-DD): ").strip()
        kilometraje = int(input("Kilometraje: "))
        modelo = int(input("Modelo (ID): "))
        
        success = create_row(
            "autos", 
            ["patente", "precio", "auto_prueba", "disponible", "fecha_llegada", "kilometraje", "modelo"],
            [patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, modelo]
        )
        
        if success:
            print("✓ Auto creado exitosamente.")
        else:
            print("✗ Error al crear el auto.")
            
    except ValueError as e:
        print(f"Error: Valor inválido ingresado - {e}")
    except Exception as e:
        print(f"Error inesperado al crear el auto: {e}")
    
    input("\nPresione Enter para continuar...")

def leer_autos():
    """Lee y muestra todos los autos de la base de datos"""
    limpiar_consola()
    try:
        print("=== Lista de Autos ===")
        colnames, rows = read_rows("autos")
        
        if colnames is None or rows is None:
            print("Error al obtener los datos de autos.")
            input("\nPresione Enter para continuar...")
            return
        
        if not rows:
            print("No hay autos registrados en la base de datos.")
            input("\nPresione Enter para continuar...")
            return
        
        # Mostrar encabezados
        print("\n" + " | ".join(colnames))
        print("-" * (len(" | ".join(colnames)) + 10))
        
        # Mostrar datos
        for row in rows:
            print(" | ".join(str(cell) for cell in row))
        
        print(f"\nTotal de autos: {len(rows)}")
        
    except Exception as e:
        print(f"Error al leer los autos: {e}")
    
    input("\nPresione Enter para continuar...")

def actualizar_auto():
    """Actualiza un auto existente en la base de datos"""
    limpiar_consola()
    try:
        print("=== Actualizar Auto ===")
        
        # Mostrar autos disponibles primero
        print("Autos disponibles:")
        colnames, rows = read_rows("autos", ["patente", "precio", "disponible"])
        
        if not rows:
            print("No hay autos para actualizar.")
            input("\nPresione Enter para continuar...")
            return
        
        for row in rows:
            print(f"Patente: {row[0]}, Precio: {row[1]}, Disponible: {row[2]}")
        
        print("\n" + "="*50)
        patente = input("Patente (PK) del auto a actualizar: ").strip().upper()
        
        # Verificar que el auto existe
        colnames, existing = read_rows("autos", where_clause="patente = %s", where_values=[patente])
        if not existing:
            print(f"No se encontró un auto con patente {patente}")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nCampos disponibles para actualizar:")
        campos_disponibles = ["precio", "auto_prueba", "disponible", "fecha_llegada", "kilometraje", "modelo"]
        for i, campo in enumerate(campos_disponibles, 1):
            print(f"{i}. {campo}")
        
        opcion = input("\nSeleccione el número del campo a actualizar: ").strip()
        
        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(campos_disponibles):
                campo = campos_disponibles[indice]
                valor = input(f"Nuevo valor para {campo}: ").strip()
                
                # Convertir el valor según el tipo de campo
                if campo == "precio":
                    valor = float(valor)
                elif campo in ["auto_prueba", "disponible"]:
                    valor = valor.lower() == 'true'
                elif campo in ["kilometraje", "modelo"]:
                    valor = int(valor)
                
                success = update_row("autos", "patente", patente, [campo], [valor])
                
                if success:
                    print("✓ Auto actualizado exitosamente.")
                else:
                    print("✗ No se pudo actualizar el auto.")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            
    except Exception as e:
        print(f"Error al actualizar el auto: {e}")
    
    input("\nPresione Enter para continuar...")

def eliminar_auto():
    """Marca un auto como no disponible (eliminación lógica)"""
    limpiar_consola()
    try:
        print("=== Eliminar Auto (Marcar como No Disponible) ===")
        
        # Mostrar autos disponibles
        colnames, rows = read_rows("autos", ["patente", "precio", "disponible"], 
                                  where_clause="disponible = true")
        
        if not rows:
            print("No hay autos disponibles para eliminar.")
            input("\nPresione Enter para continuar...")
            return
        
        print("Autos disponibles:")
        for row in rows:
            print(f"Patente: {row[0]}, Precio: {row[1]}")
        
        print("\n" + "="*50)
        patente = input("Patente del auto a marcar como no disponible: ").strip().upper()
        
        # Confirmar la acción
        confirmar = input(f"¿Está seguro de marcar el auto {patente} como no disponible? (s/n): ").strip().lower()
        
        if confirmar == 's':
            success = update_row("autos", "patente", patente, ["disponible"], [False])
            
            if success:
                print("✓ Auto marcado como no disponible exitosamente.")
            else:
                print("✗ No se pudo marcar el auto como no disponible.")
        else:
            print("Operación cancelada.")
            
    except Exception as e:
        print(f"Error al eliminar el estado del auto: {e}")
    
    input("\nPresione Enter para continuar...")

def buscar_auto_por_patente(patente):
    """
    Busca un auto específico por su patente.
    
    Args:
        patente (str): Patente del auto a buscar
    
    Returns:
        dict: Información del auto o None si no se encuentra
    """
    try:
        colnames, rows = read_rows("autos", where_clause="patente = %s", where_values=[patente])
        
        if rows:
            # Convertir a diccionario para mayor facilidad de uso
            auto_dict = dict(zip(colnames, rows[0]))
            return auto_dict
        return None
    except Exception as e:
        print(f"Error al buscar auto: {e}")
        return None

def listar_autos_disponibles():
    """
    Lista solo los autos que están disponibles.
    
    Returns:
        list: Lista de autos disponibles
    """
    try:
        colnames, rows = read_rows("autos", where_clause="disponible = true")
        if rows:
            return [dict(zip(colnames, row)) for row in rows]
        return []
    except Exception as e:
        print(f"Error al listar autos disponibles: {e}")
        return []
