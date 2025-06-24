from config import get_connection
import schedule
import time

def extract():
    conn = get_connection()
    cur = conn.cursor()
    # Extrae los datos necesarios del modelo transaccional
    cur.execute("""
        SELECT v.id_venta, v.id_concesionaria, v.id_usuario, v.id_auto, v.monto, v.fecha_venta, a.precio
        FROM ventas v
        JOIN autos a ON v.id_auto = a.patente
    """)
    datos = cur.fetchall()
    cur.close()
    conn.close()
    return datos

def transform(datos):
    # Aquí puedes transformar los datos si es necesario
    # Por ejemplo, podrías calcular márgenes, formatos de fecha, etc.
    # En este ejemplo, solo los pasamos tal cual
    return datos

def load(datos):
    conn = get_connection()
    cur = conn.cursor()
    # 1. Elimina todos los datos de la tabla de hechos
    cur.execute("DELETE FROM hechos_ventas")
    # 2. Inserta los datos transformados
    for fila in datos:
        cur.execute("""
            INSERT INTO hechos_ventas (id_venta, id_concesionaria, id_usuario, id_auto, monto, fecha_venta, precio_auto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, fila)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabla de hechos actualizada.")

def main():
    datos = extract()
    datos_transformados = transform(datos)
    load(datos_transformados)

def job():
    print("Ejecutando ETL programado...")
    main()

if __name__ == "__main__":
    # Programa el ETL para que corra todos los días a las 2:00 AM
    schedule.every().day.at("02:00").do(job)
    print("Scheduler iniciado. Presiona Ctrl+C para detener.")
    while True:
        schedule.run_pending()
        time.sleep(60)