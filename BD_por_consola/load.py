from db_utils import execute_query

def load_modelos(data):
    for row in data:
        query = """
            INSERT INTO analisis.modelos
            (id_modelo, nombre_modelo, cantidad_puertas, tipo_vehiculo, numero_pasajeros, octanaje, maletero, traccion, marca)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_modelo) DO NOTHING
        """
        params = (
            row["id_modelo"], row["nombre_modelo"], row["cantidad_puertas"], row["tipo_vehiculo"],
            row["numero_pasajeros"], row["octanaje"], row["maletero"], row["traccion"], row["marca"]
        )
        execute_query(query, params)

def load_autos(data):
    for row in data:
        query = """
            INSERT INTO analisis.autos
            (patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, modelo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (patente) DO NOTHING
        """
        params = (
            row["patente"], row["precio"], row["auto_prueba"], row["disponible"],
            row["fecha_llegada"], row["kilometraje"], row["modelo"]
        )
        execute_query(query, params)

def load_concesionarias(data):
    for row in data:
        query = """
            INSERT INTO analisis.concesionarias
            (id_concesionarias, direccion, capacidad_vehicular)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_concesionarias) DO NOTHING
        """
        params = (
            row["id_concesionarias"], row["direccion"], row["capacidad_vehicular"]
        )
        execute_query(query, params)

def load_usuarios(data):
    for row in data:
        query = """
            INSERT INTO analisis.usuarios
            (rut, nombre, apellido, profesion, socio)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (rut) DO NOTHING
        """
        params = (
            row["rut"], row["nombre"], row["apellido"], row["profesion"], row["socio"]
        )
        execute_query(query, params)

def load_region(data):
    for row in data:
        query = """
            INSERT INTO analisis.region
            (id_region, nombre_region)
            VALUES (%s, %s)
            ON CONFLICT (id_region) DO NOTHING
        """
        params = (
            row["id_region"], row["nombre_region"]
        )
        execute_query(query, params)

def load_comunas(data):
    for row in data:
        query = """
            INSERT INTO analisis.comunas
            (id_comuna, nombre_comuna)
            VALUES (%s, %s)
            ON CONFLICT (id_comuna) DO NOTHING
        """
        params = (
            row["id_comuna"], row["nombre_comuna"]
        )
        execute_query(query, params)

def load_ciudades(data):
    for row in data:
        query = """
            INSERT INTO analisis.ciudades
            (id_ciudades, nombre_ciudades)
            VALUES (%s, %s)
            ON CONFLICT (id_ciudades) DO NOTHING
        """
        params = (
            row["id_ciudades"], row["nombre_ciudades"]
        )
        execute_query(query, params)

def load_hechos_compras(data):
    for row in data:
        query = """
            INSERT INTO analisis."Hechos_compras"
            (id_compras, fecha_compra, monto, id_concesionaria, id_auto, id_modelo, id_ciudad, id_region, id_comuna)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_compras) DO NOTHING
        """
        params = (
            row["id_compras"], row["fecha_compra"], row["monto"], row["id_concesionaria"],
            row["id_auto"], row["id_modelo"], row["id_ciudad"], row["id_region"], row["id_comuna"]
        )
        execute_query(query, params)

def load_hechos_ventas(data):
    for row in data:
        query = """
            INSERT INTO analisis.hechos_ventas
            (id_venta, id_concesionaria, id_usuario, id_auto, monto, fecha_venta, id_modelo, id_ciudad, id_region, id_comuna)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_venta) DO NOTHING
        """
        params = (
            row["id_venta"],
            row["id_concesionaria"],
            row["id_usuario"],
            row["id_auto"],
            row["monto"],
            row["fecha_venta"],
            row["id_modelo"],
            row["id_ciudad"],
            row["id_region"],
            row["id_comuna"]
        )
        execute_query(query, params)