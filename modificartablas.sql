CREATE SCHEMA IF NOT EXISTS analisis;

SET search_path TO analisis;

-- Crear tabla modelos
CREATE TABLE IF NOT EXISTS modelos (
    id_modelo SERIAL PRIMARY KEY,
    nombre_modelo VARCHAR,
    cantidad_puertas INTEGER,
    tipo_vehiculo VARCHAR,
    numero_pasajeros INTEGER,
    octanaje VARCHAR,
    maletero VARCHAR,
    traccion VARCHAR,
    marca VARCHAR
);

-- Crear tabla autos
CREATE TABLE IF NOT EXISTS autos (
    patente VARCHAR PRIMARY KEY,
    precio DOUBLE PRECISION,
    auto_prueba BOOLEAN,
    disponible BOOLEAN,
    fecha_llegada TIMESTAMP,
    kilometraje INTEGER,
    modelo INTEGER REFERENCES modelos(id_modelo)
);

-- Crear tabla concesionarias
CREATE TABLE IF NOT EXISTS concesionarias (
    id_concesionarias INTEGER PRIMARY KEY,
    direccion VARCHAR,
    capacidad_vehicular INTEGER
);

-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    rut INTEGER PRIMARY KEY,
    nombre VARCHAR,
    apellido VARCHAR,
    profesion VARCHAR,
    socio BOOLEAN
);

-- Crear tabla Hechos_compras
CREATE TABLE IF NOT EXISTS "Hechos_compras" (
    id_compras SERIAL PRIMARY KEY,
    fecha_compra TIMESTAMP,
    monto DOUBLE PRECISION,
    id_concesionaria INTEGER REFERENCES concesionarias(id_concesionarias),
    id_auto VARCHAR REFERENCES autos(patente),
    id_modelo INTEGER REFERENCES modelos(id_modelo),
    id_ciudad INTEGER REFERENCES ciudades (id_ciudades),
    id_region INTEGER REFERENCES region (id_region),
    id_comuna INTEGER REFERENCES comunas (id_comuna)
);

-- Crear tabla Hechos_ventas
CREATE TABLE IF NOT EXISTS Hechos_ventas (
    id_venta SERIAL PRIMARY KEY,
    id_concesionaria INTEGER REFERENCES concesionarias(id_concesionarias),
    id_usuario INTEGER REFERENCES usuarios(rut),
    id_auto VARCHAR REFERENCES autos(patente),
    monto DOUBLE PRECISION,
    fecha_venta TIMESTAMP,
    id_modelo INTEGER REFERENCES modelos(id_modelo),
    id_ciudad INTEGER,
    id_region INTEGER,
    id_comuna INTEGER
);


--crea la tabla region
CREATE TABLE IF NOT EXISTS region (
    id_region INTEGER PRIMARY KEY,
    nombre_region VARCHAR
);

CREATE TABLE IF NOT EXISTS ciudades (
    id_ciudades INTEGER PRIMARY KEY,
    nombre_ciudades VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS comunas (
    id_comuna INTEGER PRIMARY KEY,
    nombre_comuna VARCHAR NOT NULL
);
