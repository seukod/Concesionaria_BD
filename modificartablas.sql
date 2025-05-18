-- Crear tabla modelos
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

-- Crear tabla autos
CREATE TABLE autos (
    patente VARCHAR PRIMARY KEY,
    precio DOUBLE PRECISION,
    auto_prueba BOOLEAN,
    disponible BOOLEAN,
    fecha_llegada TIMESTAMP,
    kilometraje INTEGER,
    modelo INTEGER REFERENCES modelos(id_modelo)
);

-- Crear tabla concesionarias
CREATE TABLE concesionarias (
    id_concesionarias INTEGER PRIMARY KEY,
    direccion VARCHAR,
    capacidad_vehicular INTEGER
);

-- Crear tabla usuarios
CREATE TABLE usuarios (
    rut INTEGER PRIMARY KEY,
    nombre VARCHAR,
    apellido VARCHAR,
    profesion VARCHAR,
    socio BOOLEAN
);

-- Crear tabla Hechos_compras
CREATE TABLE Hechos_compras (
    id_compras SERIAL PRIMARY KEY,
    fecha_compra TIMESTAMP,
    monto DOUBLE PRECISION,
    concesionaria INTEGER, -- (No tiene FK definida, puede eliminarse o normalizarse)
    id_auto VARCHAR REFERENCES autos(patente),
    id_modelo INTEGER REFERENCES modelos(id_modelo),
    id_concesionaria VARCHAR, -- (No tiene FK definida)
    id_ciudad INTEGER,
    id_region INTEGER,
    id_comuna INTEGER
);

-- Crear tabla Hechos_ventas
CREATE TABLE Hechos_ventas (
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
CREATE TABLE region (
    id_region INTEGER PRIMARY KEY,
    nombre_region VARCHAR
);

--conecta la tabla region con compras
ALTER TABLE "Hechos_compras"
ADD CONSTRAINT fk_hechoscompras_region
FOREIGN KEY (id_region)
REFERENCES region (id_region);

--conecta la tabla region con compras
ALTER TABLE "Hechos_ventas"
ADD CONSTRAINT fk_hechosventas_region
FOREIGN KEY (id_region)
REFERENCES region (id_region);


--crear la tabla ciudades
CREATE TABLE ciudades (
    id_ciudades INTEGER PRIMARY KEY,
    nombre_ciudades VARCHAR NOT NULL
);


--crear tabla comunas
CREATE TABLE comunas (
    id_comuna INTEGER PRIMARY KEY,
    nombre_comuna VARCHAR NOT NULL
);


-- Para Hechos_compras con ciudades y comunas
ALTER TABLE "Hechos_compras"
ADD CONSTRAINT fk_hechoscompras_comuna
FOREIGN KEY (id_comuna)
REFERENCES comunas (id_comuna);

ALTER TABLE "Hechos_compras"
ADD CONSTRAINT fk_hechoscompras_ciudad
FOREIGN KEY (id_ciudad)
REFERENCES ciudades (id_ciudades);

-- Para Hechos_ventas con ciudades y comunas
ALTER TABLE "Hechos_ventas"
ADD CONSTRAINT fk_hechosventas_comuna
FOREIGN KEY (id_comuna)
REFERENCES comunas (id_comuna);

ALTER TABLE "Hechos_ventas"
ADD CONSTRAINT fk_hechosventas_ciudad
FOREIGN KEY (id_ciudad)
REFERENCES ciudades (id_ciudades);