import psycopg2
from config import DB_CONFIG

def extract_modelos():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id_modelo, nombre_modelo, cantidad_puertas, tipo_vehiculo, numero_pasajeros, octanaje, maletero, traccion, marca
        FROM transaccional.modelos
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_modelo": row[0],
            "nombre_modelo": row[1],
            "cantidad_puertas": row[2],
            "tipo_vehiculo": row[3],
            "numero_pasajeros": row[4],
            "octanaje": row[5],
            "maletero": row[6],
            "traccion": row[7],
            "marca": row[8]
        }
        for row in rows
    ]

def extract_autos():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, modelo
        FROM transaccional.autos
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "patente": row[0],
            "precio": row[1],
            "auto_prueba": row[2],
            "disponible": row[3],
            "fecha_llegada": row[4],
            "kilometraje": row[5],
            "modelo": row[6]
        }
        for row in rows
    ]

def extract_concesionarias():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id_concesionarias, direccion
        FROM transaccional.concesionarias
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_concesionarias": row[0],
            "direccion": row[1],
            "capacidad_vehicular": 0  # Puedes calcularlo si tienes la lógica
        }
        for row in rows
    ]

def extract_usuarios():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT rut, nombre, apellido, profesion, socio
        FROM transaccional.usuarios
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "rut": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "profesion": row[3],
            "socio": row[4]
        }
        for row in rows
    ]

def extract_region():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id_region, nombre_region
        FROM transaccional.region
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_region": row[0],
            "nombre_region": row[1]
        }
        for row in rows
    ]

def extract_comunas():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id_comuna, nombre_comuna
        FROM transaccional.comuna
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_comuna": row[0],
            "nombre_comuna": row[1]
        }
        for row in rows
    ]

def extract_ciudades():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id_ciudad, nombre_ciudad
        FROM transaccional.ciudad
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_ciudades": row[0],
            "nombre_ciudades": row[1]
        }
        for row in rows
    ]

def extract_hechos_compras():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.id_compras, 
            c.fecha_compra, 
            c.monto, 
            c.concesionaria AS id_concesionaria,
            a.modelo AS id_modelo,
            coalesce(ci.id_ciudad, NULL) AS id_ciudad,
            coalesce(r.id_region, NULL) AS id_region,
            coalesce(cm.id_comuna, NULL) AS id_comuna,
            c.id_auto
        FROM transaccional.compras c
        LEFT JOIN transaccional.autos a ON c.id_auto = a.patente
        LEFT JOIN transaccional.concesionarias cons ON c.concesionaria = cons.id_concesionarias
        LEFT JOIN transaccional.ciudad ci ON cons.id_ciudad_concesionaria = ci.id_ciudad
        LEFT JOIN transaccional.comuna cm ON ci.id_comuna_perteneciente = cm.id_comuna
        LEFT JOIN transaccional.region r ON cm.id_region_perteneciente = r.id_region
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_compras": row[0],
            "fecha_compra": row[1],
            "monto": row[2],
            "id_concesionaria": row[3],
            "id_auto": row[8],
            "id_modelo": row[4],
            "id_ciudad": row[5],
            "id_region": row[6],
            "id_comuna": row[7]
        }
        for row in rows
    ]

def extract_hechos_ventas():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            v.id_venta, 
            c.id_concesionarias AS id_concesionaria,
            ci.id_comuna
        FROM transaccional.ventas v
        LEFT JOIN transaccional.compras comp ON v.id_venta = comp.id_compras
        LEFT JOIN transaccional.concesionarias c ON comp.concesionaria = c.id_concesionarias
        LEFT JOIN transaccional.ciudad cd ON c.id_ciudad_concesionaria = cd.id_ciudad
        LEFT JOIN transaccional.comuna ci ON cd.id_comuna_perteneciente = ci.id_comuna
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id_venta": row[0],
            "id_concesionaria": row[1],
            "id_comuna": row[2]
        }
        for row in rows
    ]