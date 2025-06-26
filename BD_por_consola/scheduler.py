"""
Sistema de Schedule Simple para Base de Datos de Concesionaria
Ejecuta tareas automatizadas los domingos

Este script está diseñado para estudiantes de base de datos.
Implementación simple y fácil de entender.
"""

import schedule
import time
import datetime
from etl import run_etl
from config import DB_CONFIG
import psycopg2
import logging
import os

# Configurar logging para registrar las ejecuciones
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'scheduler.log')),
        logging.StreamHandler()
    ]
)

def ejecutar_limpieza_semanal():
    """
    Tarea de limpieza semanal que se ejecuta los domingos
    - Limpia logs antiguos
    - Ejecuta VACUUM en la base de datos
    - Actualiza estadísticas
    """
    try:
        logging.info("=== INICIANDO LIMPIEZA SEMANAL DOMINICAL ===")
        
        # 1. Limpiar logs antiguos (más de 30 días)
        limpiar_logs_antiguos()
        
        # 2. Ejecutar VACUUM en la base de datos
        ejecutar_vacuum_db()
        
        # 3. Actualizar estadísticas de la base de datos
        actualizar_estadisticas_db()
        
        logging.info("=== LIMPIEZA SEMANAL COMPLETADA EXITOSAMENTE ===")
        
    except Exception as e:
        logging.error(f"Error durante la limpieza semanal: {e}")

def ejecutar_etl_semanal():
    """
    Ejecuta el proceso ETL semanalmente los domingos
    """
    try:
        logging.info("=== INICIANDO ETL SEMANAL DOMINICAL ===")
        run_etl()
        logging.info("=== ETL SEMANAL COMPLETADO EXITOSAMENTE ===")
        
    except Exception as e:
        logging.error(f"Error durante el ETL semanal: {e}")

def limpiar_logs_antiguos():
    """
    Elimina archivos de log más antiguos de 30 días
    """
    try:
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(log_dir):
            return
            
        ahora = datetime.datetime.now()
        archivos_eliminados = 0
        
        for archivo in os.listdir(log_dir):
            ruta_archivo = os.path.join(log_dir, archivo)
            if os.path.isfile(ruta_archivo):
                fecha_archivo = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
                if (ahora - fecha_archivo).days > 30:
                    os.remove(ruta_archivo)
                    archivos_eliminados += 1
        
        logging.info(f"Limpieza de logs: {archivos_eliminados} archivos eliminados")
        
    except Exception as e:
        logging.error(f"Error al limpiar logs antiguos: {e}")

def ejecutar_vacuum_db():
    """
    Ejecuta VACUUM en la base de datos para optimizar el espacio
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        # VACUUM en esquema transaccional
        cur.execute("VACUUM ANALYZE transaccional.autos;")
        cur.execute("VACUUM ANALYZE transaccional.ventas;")
        
        # VACUUM en esquema de análisis
        cur.execute("VACUUM ANALYZE analisis.hechos_ventas;")
        cur.execute("VACUUM ANALYZE analisis.\"Hechos_compras\";")
        
        cur.close()
        conn.close()
        
        logging.info("VACUUM ejecutado exitosamente en todas las tablas principales")
        
    except Exception as e:
        logging.error(f"Error al ejecutar VACUUM: {e}")

def actualizar_estadisticas_db():
    """
    Actualiza las estadísticas de la base de datos
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Obtener estadísticas básicas
        cur.execute("""
            SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
            FROM pg_stat_user_tables 
            WHERE schemaname IN ('transaccional', 'analisis')
            ORDER BY schemaname, tablename;
        """)
        
        estadisticas = cur.fetchall()
        
        logging.info("=== ESTADÍSTICAS DE TABLAS ===")
        for stat in estadisticas:
            schema, tabla, inserts, updates, deletes = stat
            logging.info(f"{schema}.{tabla}: Inserts={inserts}, Updates={updates}, Deletes={deletes}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"Error al obtener estadísticas: {e}")

def generar_reporte_semanal():
    """
    Genera un reporte semanal simple del estado de la base de datos
    """
    try:
        logging.info("=== GENERANDO REPORTE SEMANAL ===")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Contar registros en tablas principales
        cur.execute("SELECT COUNT(*) FROM transaccional.autos;")
        total_autos = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM transaccional.ventas;")
        total_ventas = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM analisis.hechos_ventas;")
        total_hechos_ventas = cur.fetchone()[0]
        
        # Última venta registrada
        cur.execute("SELECT MAX(fecha_venta) FROM transaccional.ventas;")
        ultima_venta = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        # Log del reporte
        logging.info(f"REPORTE SEMANAL - {datetime.datetime.now().strftime('%Y-%m-%d')}")
        logging.info(f"Total de autos: {total_autos}")
        logging.info(f"Total de ventas: {total_ventas}")
        logging.info(f"Total de hechos de ventas (análisis): {total_hechos_ventas}")
        logging.info(f"Última venta registrada: {ultima_venta}")
        
    except Exception as e:
        logging.error(f"Error al generar reporte semanal: {e}")

def mostrar_proximo_domingo():
    """
    Muestra cuándo será la próxima ejecución (domingo)
    """
    hoy = datetime.datetime.now()
    dias_hasta_domingo = (6 - hoy.weekday()) % 7
    if dias_hasta_domingo == 0 and hoy.hour < 10:  # Si es domingo y son menos de las 10 AM
        dias_hasta_domingo = 0
    elif dias_hasta_domingo == 0:  # Si es domingo pero ya pasó la hora
        dias_hasta_domingo = 7
    
    proximo_domingo = hoy + datetime.timedelta(days=dias_hasta_domingo)
    proximo_domingo = proximo_domingo.replace(hour=10, minute=0, second=0, microsecond=0)
    
    print(f"📅 Próxima ejecución programada: {proximo_domingo.strftime('%A %d de %B de %Y a las %H:%M')}")
    return proximo_domingo

def configurar_schedule():
    """
    Configura las tareas programadas para los domingos
    """
    # Programar tareas para los domingos a las 10:00 AM
    schedule.every().sunday.at("10:00").do(ejecutar_etl_semanal)
    schedule.every().sunday.at("10:30").do(ejecutar_limpieza_semanal)
    schedule.every().sunday.at("11:00").do(generar_reporte_semanal)
    
    print("✅ Schedule configurado exitosamente!")
    print("📋 Tareas programadas para los domingos:")
    print("   • 10:00 AM - ETL Semanal")
    print("   • 10:30 AM - Limpieza de Base de Datos")
    print("   • 11:00 AM - Reporte Semanal")
    
    mostrar_proximo_domingo()

def ejecutar_scheduler():
    """
    Función principal que ejecuta el scheduler
    """
    print("\n" + "="*60)
    print("        SCHEDULER DE BASE DE DATOS - CONCESIONARIA")
    print("="*60)
    print("🕐 Iniciando sistema de tareas programadas...")
    
    configurar_schedule()
    
    print("\n⚡ Scheduler en ejecución. Presiona Ctrl+C para detener.")
    print("📊 Las tareas se ejecutarán automáticamente los domingos.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
            
    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler detenido por el usuario.")
        logging.info("Scheduler detenido manualmente")

def ejecutar_tareas_ahora():
    """
    Función para ejecutar todas las tareas inmediatamente (para pruebas)
    """
    print("\n🧪 MODO DE PRUEBA - Ejecutando todas las tareas ahora...")
    print("="*50)
    
    try:
        ejecutar_etl_semanal()
        print("✅ ETL completado")
        
        ejecutar_limpieza_semanal()
        print("✅ Limpieza completada")
        
        generar_reporte_semanal()
        print("✅ Reporte generado")
        
        print("\n🎉 Todas las tareas de prueba completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    print("🚀 Sistema de Schedule de Base de Datos")
    print("Selecciona una opción:")
    print("1. Iniciar scheduler (ejecutar los domingos)")
    print("2. Ejecutar tareas ahora (modo prueba)")
    print("3. Mostrar próxima ejecución")
    
    opcion = input("Opción: ").strip()
    
    if opcion == "1":
        ejecutar_scheduler()
    elif opcion == "2":
        ejecutar_tareas_ahora()
    elif opcion == "3":
        mostrar_proximo_domingo()
    else:
        print("❌ Opción no válida")
