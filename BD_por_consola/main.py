import os
from config import *
from autos import *
from ventas import *
from etl import run_etl
from crud_utils import limpiar_consola

def mostrar_menu_principal():
    """Muestra el menú principal de la aplicación"""
    print("\n" + "="*50)
    print("      SISTEMA DE GESTIÓN DE CONCESIONARIA")
    print("="*50)
    print("1. Actualizaciones (compras/ventas)")
    print("2. Rellenar base de datos transaccional")
    print("3. Ejecutar ETL")
    print("4. Diagnóstico de rendimiento")
    print("5. Sistema de Schedule (Tareas Automáticas)")
    print("6. Salir")
    print("="*50)

def mostrar_menu_modificaciones():
    """Muestra el menú de modificaciones CRUD"""
    print("\n" + "="*40)
    print("         MENÚ DE MODIFICACIONES")
    print("="*40)
    print("1. CRUD tabla Autos")
    print("2. CRUD tabla de Ventas")
    print("3. Volver al menú principal")
    print("="*40)

def mostrar_menu_crud(tabla):
    """Muestra el menú CRUD específico para una tabla"""
    print(f"\n" + "="*40)
    print(f"      GESTIÓN DE {tabla.upper()}")
    print("="*40)
    print("1. Crear nuevo registro")
    print("2. Leer/Listar registros")
    print("3. Actualizar registro")
    print("4. Eliminar registro")
    print("5. Volver al menú anterior")
    print("="*40)

def opcion_modificacion(tabla):
    """
    Maneja las opciones CRUD para una tabla específica.
    
    Args:
        tabla (str): Nombre de la tabla ('autos' o 'ventas')
    """
    while True:
        try:
            limpiar_consola()
            mostrar_menu_crud(tabla)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "5":
                return
            
            limpiar_consola()
            
            if tabla == "autos":
                ejecutar_operacion_autos(opcion)
            elif tabla == "ventas":
                ejecutar_operacion_ventas(opcion)
            else:
                print("Tabla no reconocida.")
                input("\nPresione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para continuar...")
        except Exception as e:
            print(f"Error inesperado: {e}")
            input("\nPresione Enter para continuar...")

def ejecutar_operacion_autos(opcion):
    """Ejecuta operaciones CRUD específicas para autos"""
    operaciones = {
        "1": crear_auto,
        "2": leer_autos,
        "3": actualizar_auto,
        "4": eliminar_auto
    }
    
    if opcion in operaciones:
        operaciones[opcion]()
    else:
        print("❌ Opción no válida. Intente de nuevo.")
        input("\nPresione Enter para continuar...")

def ejecutar_operacion_ventas(opcion):
    """Ejecuta operaciones CRUD específicas para ventas"""
    operaciones = {
        "1": crear_venta,
        "2": leer_ventas,
        "3": actualizar_venta,
        "4": eliminar_venta
    }
    
    if opcion in operaciones:
        operaciones[opcion]()
    else:
        print("❌ Opción no válida. Intente de nuevo.")
        input("\nPresione Enter para continuar...")

def menu_modificaciones():
    """Maneja el menú principal de modificaciones"""
    while True:
        try:
            limpiar_consola()
            mostrar_menu_modificaciones()
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                opcion_modificacion("autos")
            elif opcion == "2":
                opcion_modificacion("ventas")
            elif opcion == "3":
                return
            else:
                print("❌ Opción no válida. Intente de nuevo.")
                input("\nPresione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nVolviendo al menú anterior...")
            return
        except Exception as e:
            print(f"Error inesperado: {e}")
            input("\nPresione Enter para continuar...")

def rellenar_base_datos():
    """Ejecuta el script SQL para rellenar la base de datos transaccional"""
    try:
        sql_path = os.path.join(os.path.dirname(__file__), '..', 'ingresar_datos_tra.sql')
        sql_path = os.path.abspath(sql_path)
        
        if not os.path.exists(sql_path):
            print(f"❌ Error: No se encontró el archivo SQL en {sql_path}")
            input("\nPresione Enter para continuar...")
            return
        
        print(f"📄 Ejecutando script SQL: {sql_path}")
        print("⏳ Por favor espere...")
        
        import psycopg2
        from config import DB_CONFIG

        with open(sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Base de datos rellenada exitosamente.")
        
    except FileNotFoundError:
        print("❌ Error: Archivo SQL no encontrado.")
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al ejecutar el script SQL: {e}")
    
    input("\nPresione Enter para continuar...")

def ejecutar_etl():
    """Ejecuta el proceso ETL"""
    try:
        print("🔄 Iniciando proceso ETL...")
        print("⏳ Por favor espere...")
        run_etl()
        print("✅ Proceso ETL completado.")
    except Exception as e:
        print(f"❌ Error durante el proceso ETL: {e}")
    
    input("\nPresione Enter para continuar...")

def inicializar_sistema():
    """Inicializa el sistema creando la base de datos y esquemas necesarios"""
    try:
        print("🔧 Inicializando sistema...")
        print("📊 Creando base de datos si no existe...")
        create_database_if_not_exists()
        
        print("📋 Ejecutando scripts de esquema...")
        run_schema_scripts()
        
        print("✅ Sistema inicializado correctamente.")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        print("El sistema puede no funcionar correctamente.")
        input("\nPresione Enter para continuar de todos modos...")

def ejecutar_diagnostico():
    """Ejecuta el diagnóstico de rendimiento del sistema"""
    try:
        print("🔍 Iniciando diagnóstico de rendimiento...")
        print("⏳ Por favor espere...")
        
        # Importar y ejecutar diagnóstico
        from diagnostico_performance import benchmark_database_operations, show_pool_information
        
        benchmark_database_operations()
        show_pool_information()
        
        print("✅ Diagnóstico completado.")
    except ImportError:
        print("❌ Error: Módulo de diagnóstico no encontrado.")
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
    
    input("\nPresione Enter para continuar...")

def mostrar_menu_schedule():
    """Muestra el menú del sistema de schedule"""
    print("\n" + "="*50)
    print("      SISTEMA DE SCHEDULE - TAREAS AUTOMÁTICAS")
    print("="*50)
    print("1. Iniciar scheduler (ejecutar los domingos)")
    print("2. Ejecutar tareas ahora (modo prueba)")
    print("3. Ver próxima ejecución programada")
    print("4. Volver al menú principal")
    print("="*50)

def menu_schedule():
    """Maneja el menú del sistema de schedule"""
    while True:
        try:
            limpiar_consola()
            mostrar_menu_schedule()
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                limpiar_consola()
                try:
                    from scheduler import ejecutar_scheduler
                    ejecutar_scheduler()
                except ImportError:
                    print("❌ Error: No se pudo importar el módulo scheduler.")
                    print("Asegúrese de que la librería 'schedule' esté instalada.")
                    input("\nPresione Enter para continuar...")
                except Exception as e:
                    print(f"❌ Error al ejecutar el scheduler: {e}")
                    input("\nPresione Enter para continuar...")
                    
            elif opcion == "2":
                limpiar_consola()
                try:
                    from scheduler import ejecutar_tareas_ahora
                    ejecutar_tareas_ahora()
                except ImportError:
                    print("❌ Error: No se pudo importar el módulo scheduler.")
                    input("\nPresione Enter para continuar...")
                except Exception as e:
                    print(f"❌ Error al ejecutar las tareas: {e}")
                    input("\nPresione Enter para continuar...")
                    
            elif opcion == "3":
                limpiar_consola()
                try:
                    from scheduler import mostrar_proximo_domingo
                    mostrar_proximo_domingo()
                except ImportError:
                    print("❌ Error: No se pudo importar el módulo scheduler.")
                except Exception as e:
                    print(f"❌ Error: {e}")
                input("\nPresione Enter para continuar...")
                
            elif opcion == "4":
                return
            else:
                print("❌ Opción no válida. Intente de nuevo.")
                input("\nPresione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nVolviendo al menú anterior...")
            return
        except Exception as e:
            print(f"Error inesperado: {e}")
            input("\nPresione Enter para continuar...")

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar el sistema
        inicializar_sistema()
        
        # Menú principal
        while True:
            try:
                limpiar_consola()
                mostrar_menu_principal()
                
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "1":
                    menu_modificaciones()
                elif opcion == "2":
                    limpiar_consola()
                    rellenar_base_datos()
                elif opcion == "3":
                    limpiar_consola()
                    ejecutar_etl()
                elif opcion == "4":
                    limpiar_consola()
                    ejecutar_diagnostico()
                elif opcion == "5":
                    limpiar_consola()
                    menu_schedule()
                elif opcion == "6":
                    print("👋 Saliendo del programa. ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción no válida. Intente de nuevo.")
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado en el menú principal: {e}")
                input("\nPresione Enter para continuar...")
                
    except Exception as e:
        print(f"❌ Error crítico durante la ejecución: {e}")
        print("El programa se cerrará.")
        input("\nPresione Enter para salir...")
    finally:
        # Limpiar conexiones al salir
        try:
            from db_utils import db_manager
            db_manager.close_all_connections()
        except:
            pass

if __name__ == "__main__":
    main()