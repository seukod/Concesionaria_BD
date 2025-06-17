-- Tabla región
CREATE TABLE region (
    id_region SERIAL PRIMARY KEY,
    nombre_region VARCHAR
);

-- Tabla comuna
CREATE TABLE comuna (
    id_comuna SERIAL PRIMARY KEY,
    id_region_perteneciente INTEGER REFERENCES region(id_region),
    nombre_comuna VARCHAR
);

-- Tabla ciudad
CREATE TABLE ciudad (
    id_ciudad SERIAL PRIMARY KEY,
    id_comuna_perteneciente INTEGER REFERENCES comuna(id_comuna),
    nombre_ciudad VARCHAR
);

-- Tabla concesionarias
CREATE TABLE concesionarias (
    id_concesionarias SERIAL PRIMARY KEY,
    direccion VARCHAR,
    id_ciudad_concesionaria INTEGER REFERENCES ciudad(id_ciudad)
);

-- Tabla modelos
CREATE TABLE modelos (
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

-- Tabla autos
CREATE TABLE autos (
    patente VARCHAR PRIMARY KEY,
    precio FLOAT,
    auto_prueba BOOLEAN,
    disponible BOOLEAN,
    fecha_llegada TIMESTAMP,
    kilometraje INTEGER,
    modelo INTEGER REFERENCES modelos(id_modelo)
);

-- Tabla compras
CREATE TABLE compras (
    id_compras SERIAL PRIMARY KEY,
    fecha_compra TIMESTAMP,
    monto FLOAT,
    concesionaria INTEGER REFERENCES concesionarias(id_concesionarias),
    id_auto VARCHAR REFERENCES autos(patente)
);

-- Tabla transferencias
CREATE TABLE transferencias (
    id_transferencia SERIAL PRIMARY KEY,
    desde INTEGER REFERENCES concesionarias(id_concesionarias),
    hasta INTEGER REFERENCES concesionarias(id_concesionarias),
    id_auto VARCHAR REFERENCES autos(patente),
    comentario VARCHAR
);

-- Tabla usuarios
CREATE TABLE usuarios (
    rut INTEGER PRIMARY KEY,
    nombre VARCHAR,
    apellido VARCHAR,
    profesion VARCHAR,
    socio BOOLEAN
);

-- Tabla ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_concesionaria INTEGER REFERENCES concesionarias(id_concesionarias),
    id_usuario INTEGER REFERENCES usuarios(rut),
    id_auto VARCHAR REFERENCES autos(patente),
    monto FLOAT,
    fecha_venta TIMESTAMP
);
