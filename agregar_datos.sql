--rellena la tabla region
INSERT INTO region (id_region, nombre_region) VALUES
  (1, 'Región de Tarapacá'),
  (2, 'Región de Antofagasta'),
  (3, 'Región de Atacama'),
  (4, 'Región de Coquimbo'),
  (5, 'Región de Valparaíso'),
  (6, 'Región del Libertador General Bernardo O’Higgins'),
  (7, 'Región del Maule'),
  (8, 'Región del Biobío'),
  (9, 'Región de La Araucanía'),
  (10, 'Región de Los Lagos'),
  (11, 'Región de Aysén del General Carlos Ibáñez del Campo'),
  (12, 'Región de Magallanes y de la Antártica Chilena'),
  (13, 'Región Metropolitana de Santiago'),
  (14, 'Región de Los Ríos'),
  (15, 'Región de Arica y Parinacota'),
  (16, 'Región de Ñuble');
--rellenar tablas ciudades con las 3 ciudades mas grandes de cada ciudad
INSERT INTO ciudades (id_ciudades, nombre_ciudades) VALUES
	(1, 'Arica'),(2, 'Putre'),(3, 'Camarones'),
	(4, 'Iquique'),(5, 'Alto Hospicio'),(6, 'Pozo Almonte'),
	(7, 'Antofagasta'),(8, 'Calama'),(9, 'Tocopilla'),
	(10, 'Copiapó'),(11, 'Vallenar'),(12, 'Chañaral'),
	(13, 'La Serena'),(14, 'Coquimbo'),(15, 'Ovalle'),
	(16, 'Valparaíso'),(17, 'Viña del Mar'),(18, 'Quilpué'),
	(19, 'Rancagua'),(20, 'San Fernando'),(21, 'Rengo'),
	(22, 'Talca'),(23, 'Curicó'),(24, 'Linares'),
	(25, 'Concepción'),(26, 'Talcahuano'),(27, 'Los Ángeles'),
	(28, 'Temuco'),(29, 'Villarrica'),(30, 'Angol'),
	(31, 'Valdivia'),(32, 'La Unión'),(33, 'Río Bueno'),
	(34, 'Puerto Montt'),(35, 'Osorno'),(36, 'Castro'),
	(37, 'Coyhaique'),(38, 'Puerto Aysén'),(39, 'Chile Chico'),
	(40, 'Punta Arenas'),(41, 'Puerto Natales'),(42, 'Porvenir'),
	(43, 'Santiago'),(44, 'Puente Alto'),(45, 'Maipú'),
	(46, 'Chillán'),(47, 'San Carlos'),(48, 'Bulnes');

--rellenar tablas comunas con las 3 ciudades mas grandes de cada ciudad
INSERT INTO comunas (id_comuna, nombre_comuna) VALUES
	(1, 'Arica'),(2, 'Putre'),(3, 'Camarones'),
	(4, 'Iquique'),(5, 'Alto Hospicio'),(6, 'Pozo Almonte'),
	(7, 'Antofagasta'),(8, 'Calama'),(9, 'Tocopilla'),
	(10, 'Copiapó'),(11, 'Vallenar'),(12, 'Chañaral'),
	(13, 'La Serena'),(14, 'Coquimbo'),(15, 'Ovalle'),
	(16, 'Valparaíso'),(17, 'Viña del Mar'),(18, 'Quilpué'),
	(19, 'Rancagua'),(20, 'San Fernando'),(21, 'Rengo'),
	(22, 'Talca'),(23, 'Curicó'),(24, 'Linares'),
	(25, 'Concepción'),(26, 'Talcahuano'),(27, 'Los Ángeles'),
	(28, 'Temuco'),(29, 'Villarrica'),(30, 'Angol'),
	(31, 'Valdivia'),(32, 'La Unión'),(33, 'Río Bueno'),
	(34, 'Puerto Montt'),(35, 'Osorno'),(36, 'Castro'),
	(37, 'Coyhaique'),(38, 'Puerto Aysén'),(39, 'Chile Chico'),
	(40, 'Punta Arenas'),(41, 'Puerto Natales'),(42, 'Porvenir'),
	(43, 'Santiago'),(44, 'Puente Alto'),(45, 'Maipú'),
	(46, 'Chillán'),(47, 'San Carlos'),(48, 'Bulnes');


--ingresar datos en la tabla modelos
INSERT INTO modelos (id_modelo, nombre_modelo, cantidad_puertas, tipo_vehiculo, numero_pasajeros, octanaje, maletero, traccion, marca) VALUES
(1, 'Spark GT GL', 5, 'Hatchback', 5, '93', '170L', 'Delantera', 'Chevrolet'),
(2, 'Sail GT', 5, 'Sedán', 5, '93', '362L', 'Delantera', 'Chevrolet'),
(3, 'Morning X', 5, 'Hatchback', 5, '93', '200L', 'Delantera', 'Kia'),
(4, 'Rio GL', 5, 'Sedán', 5, '95', '400L', 'Delantera', 'Kia'),
(5, 'Cerato GT', 5, 'Sedán', 5, '95', '450L', 'Delantera', 'Kia'),
(6, 'i10 GL', 5, 'Hatchback', 5, '93', '170L', 'Delantera', 'Hyundai'),
(7, 'i20 GT', 5, 'Hatchback', 5, '95', '200L', 'Delantera', 'Hyundai'),
(8, 'Accent X', 5, 'Sedán', 5, '93', '362L', 'Delantera', 'Hyundai'),
(9, 'Yaris GL', 5, 'Sedán', 5, '93', '400L', 'Delantera', 'Toyota'),
(10, 'Corolla GT', 5, 'Sedán', 5, '95', '450L', 'Delantera', 'Toyota'),
(11, 'Hilux GL', 5, 'Pick-Up', 5, '95', '450L', '4x4', 'Toyota'),
(12, 'RAV4 GT', 5, 'SUV', 5, '95', '450L', '4x4', 'Toyota'),
(13, 'Avanza GL', 5, 'SUV', 7, '93', '400L', 'Trasera', 'Toyota'),
(14, 'Vitara GL', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Suzuki'),
(15, 'Baleno X', 5, 'Hatchback', 5, '95', '200L', 'Delantera', 'Suzuki'),
(16, 'Swift GT', 5, 'Hatchback', 5, '93', '170L', 'Delantera', 'Suzuki'),
(17, 'Alto GL', 5, 'Hatchback', 4, '93', '170L', 'Delantera', 'Suzuki'),
(18, 'Celerio X', 5, 'Hatchback', 4, '93', '200L', 'Delantera', 'Suzuki'),
(19, 'Versa GT', 5, 'Sedán', 5, '93', '362L', 'Delantera', 'Nissan'),
(20, 'Sentra GL', 5, 'Sedán', 5, '95', '450L', 'Delantera', 'Nissan'),
(21, 'March X', 5, 'Hatchback', 5, '93', '170L', 'Delantera', 'Nissan'),
(22, 'X-Trail GL', 5, 'SUV', 7, '95', '450L', '4x4', 'Nissan'),
(23, 'Kicks GT', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Nissan'),
(24, '208 GL', 5, 'Hatchback', 5, '93', '200L', 'Delantera', 'Peugeot'),
(25, '301 GT', 5, 'Sedán', 5, '93', '400L', 'Delantera', 'Peugeot'),
(26, '2008 X', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Peugeot'),
(27, '3008 GL', 5, 'SUV', 5, '97', '450L', 'Delantera', 'Peugeot'),
(28, 'Partner GL', 5, 'Furgón', 2, '95', '800L', 'Delantera', 'Peugeot'),
(29, 'Fiesta GL', 5, 'Hatchback', 5, '93', '200L', 'Delantera', 'Ford'),
(30, 'Focus GT', 5, 'Sedán', 5, '95', '400L', 'Delantera', 'Ford'),
(31, 'Ecosport X', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Ford'),
(32, 'Ranger GL', 5, 'Pick-Up', 5, '95', '450L', '4x4', 'Ford'),
(33, 'Territory GT', 5, 'SUV', 5, '97', '450L', '4x4', 'Ford'),
(34, 'Kwid GL', 5, 'Hatchback', 5, '93', '170L', 'Delantera', 'Renault'),
(35, 'Stepway GT', 5, 'Hatchback', 5, '95', '210L', 'Delantera', 'Renault'),
(36, 'Duster X', 5, 'SUV', 5, '95', '400L', '4x4', 'Renault'),
(37, 'Logan GL', 5, 'Sedán', 5, '93', '362L', 'Delantera', 'Renault'),
(38, 'Captur GT', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Renault'),
(39, 'Mazda2 GL', 5, 'Hatchback', 5, '93', '200L', 'Delantera', 'Mazda'),
(40, 'Mazda3 X', 5, 'Sedán', 5, '95', '400L', 'Delantera', 'Mazda'),
(41, 'CX-3 GT', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Mazda'),
(42, 'CX-5 GL', 5, 'SUV', 5, '97', '450L', '4x4', 'Mazda'),
(43, 'BT-50 GLX', 5, 'Pick-Up', 5, '95', '450L', '4x4', 'Mazda'),
(44, 'Onix LT', 5, 'Hatchback', 5, '93', '200L', 'Delantera', 'Chevrolet'),
(45, 'Prisma LTZ', 5, 'Sedán', 5, '95', '400L', 'Delantera', 'Chevrolet'),
(46, 'Tracker Premier', 5, 'SUV', 5, '95', '362L', 'Delantera', 'Chevrolet'),
(47, 'Sportage GT', 5, 'SUV', 5, '97', '450L', '4x4', 'Kia'),
(48, 'Sorento EX', 5, 'SUV', 7, '95', '450L', '4x4', 'Kia'),
(49, 'Tucson GLS', 5, 'SUV', 5, '95', '450L', 'Delantera', 'Hyundai'),
(50, 'Elantra Premium', 5, 'Sedán', 5, '95', '400L', 'Delantera', 'Hyundai');



--rellenar la tabla autos
DO $$
DECLARE
    i INTEGER;
    letras TEXT;
    digitos TEXT;
    patente TEXT;
BEGIN
    FOR i IN 1..1000 LOOP
        letras := chr(trunc(65 + random() * 25)::int) ||
                  chr(trunc(65 + random() * 25)::int) ||
                  chr(trunc(65 + random() * 25)::int) ||
                  chr(trunc(65 + random() * 25)::int);
        digitos := lpad(trunc(random() * 99 + 1)::text, 2, '0');
        patente := letras || digitos;

        INSERT INTO autos (patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, id_modelo)
        VALUES (
            patente,
            trunc(random() * (30000000 - 5000000) + 5000000),
            (random() < 0.3),
            (random() < 0.8),
            NOW() - (trunc(random() * 1825) || ' days')::interval,
            trunc(random() * 200000),
            trunc(random() * 50 + 1)
        );
    END LOOP;
END $$;

--rellenar la tabla usuarios
DO $$
DECLARE
    i INTEGER;
    rut INTEGER;
    nombres TEXT[] := ARRAY['Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Carla', 'José', 'Camila', 'Felipe', 'Sofía', 'Diego', 'Isabel', 'Jorge', 'Lucía', 'Andrés', 'Paula', 'Ricardo', 'Claudia', 'Tomás', 'Marta'];
    apellidos TEXT[] := ARRAY['González', 'Rodríguez', 'Muñoz', 'Pérez', 'Soto', 'Rojas', 'Contreras', 'Silva', 'Martínez', 'Torres', 'Flores', 'López', 'Castillo', 'Vargas', 'Cruz', 'Molina', 'Fuentes', 'Vega', 'Orellana', 'Herrera'];
    profesiones TEXT[] := ARRAY['Ingeniero', 'Profesor', 'Médico', 'Abogado', 'Arquitecto', 'Contador', 'Periodista', 'Enfermero', 'Diseñador', 'Técnico', 'Administrativo', 'Psicólogo', 'Electrónico', 'Veterinario', 'Químico'];
BEGIN
    FOR i IN 1..150 LOOP
        rut := (random() * (25000000 - 1000000) + 1000000)::int;
        INSERT INTO usuarios (rut, nombre, apellido, profesion, socio)
        VALUES (
            rut,
            nombres[trunc(random() * array_length(nombres, 1) + 1)::int],
            apellidos[trunc(random() * array_length(apellidos, 1) + 1)::int],
            profesiones[trunc(random() * array_length(profesiones, 1) + 1)::int],
            (random() < 0.3)
        );
    END LOOP;
END $$;

--rellenar tabla consecionaria
DO $$
DECLARE
    i INTEGER;
    calles TEXT[] := ARRAY[
        'Av. Libertador Bernardo OHiggins',
        'Calle San Martín',
        'Av. Providencia',
        'Calle Alameda',
        'Calle Lira',
        'Av. Apoquindo',
        'Calle Las Heras',
        'Calle Manuel Rodríguez',
        'Av. Vitacura',
        'Calle Huérfanos',
        'Calle General Mackenna',
        'Av. Kennedy',
        'Calle Balmaceda',
        'Av. Tobalaba',
        'Calle Curicó',
        'Calle Echeñique'
    ];
BEGIN
    FOR i IN 1..48 LOOP
        INSERT INTO concesionarias (id_concesionarias, direccion, capacidad_vehicular)
        VALUES (
            i,
            calles[trunc(random() * array_length(calles, 1) + 1)::int] || ' #' || trunc(random() * 1000 + 1),
            trunc(random() * (200 - 50) + 50)  -- capacidad entre 50 y 200 vehículos
        );
    END LOOP;
END $$;


--rellenar hechos_compras
DO $$
DECLARE
    i INTEGER;
    auto_record RECORD;
    ciudad_id INTEGER;
    comuna_id INTEGER;
    region_id INTEGER;
    concesionaria_id INTEGER;
    modelo_id INTEGER;
    monto_val NUMERIC;
    fecha_compra TIMESTAMP;
BEGIN
    FOR i IN 1..1000 LOOP
        -- Elegir un auto al azar con su modelo
        SELECT * INTO auto_record FROM autos ORDER BY random() LIMIT 1;
        modelo_id := auto_record.id_modelo;
        
        -- Elegir ciudad al azar
        SELECT id_ciudades INTO ciudad_id FROM ciudades ORDER BY random() LIMIT 1;
        
        -- Calcular comuna según ciudad
        comuna_id := ((ciudad_id - 1) / 3)::int + 1;
        
        -- Calcular región según comuna (3 comunas por región)
        region_id := ((comuna_id - 1) / 3)::int + 1;
        
        -- Elegir concesionaria aleatoria
        SELECT id_concesionarias INTO concesionaria_id FROM concesionarias ORDER BY random() LIMIT 1;
        
        -- Generar un monto de compra
        monto_val := trunc(random() * (30000000 - 5000000) + 5000000);
        
        -- Fecha de compra aleatoria en últimos 5 años
        fecha_compra := NOW() - (trunc(random() * 1825) || ' days')::interval;
        
        INSERT INTO "Hechos_compras" (
            fecha_compra,
            monto,
            concesionaria,
            id_auto,
            id_modelo,
            id_concesionaria,
            id_ciudad,
            id_region,
            id_comuna
        ) VALUES (
            fecha_compra,
            monto_val,
            concesionaria_id,
            auto_record.patente,
            modelo_id,
            concesionaria_id,
            ciudad_id,
            region_id,
            comuna_id
        );
    END LOOP;
END $$;


--rellenar tabla de hechos_venta
DO $$
DECLARE
    auto_record RECORD;
    ciudad_id INTEGER;
    comuna_id INTEGER;
    region_id INTEGER;
    concesionaria_id INTEGER;
    usuario_id INTEGER;
    monto_val NUMERIC;
    fecha_venta TIMESTAMP;
BEGIN
    FOR auto_record IN
        SELECT * FROM autos WHERE disponible = false
    LOOP
        -- Elegir ciudad al azar
        SELECT id_ciudades INTO ciudad_id FROM ciudades ORDER BY random() LIMIT 1;
        
        -- Calcular comuna según ciudad (3 ciudades por comuna)
        comuna_id := ((ciudad_id - 1) / 3)::int + 1;
        
        -- Calcular región según comuna (3 comunas por región)
        region_id := ((comuna_id - 1) / 3)::int + 1;
        
        -- Elegir concesionaria aleatoria
        SELECT id_concesionarias INTO concesionaria_id FROM concesionarias ORDER BY random() LIMIT 1;
        
        -- Elegir usuario aleatorio
        SELECT rut INTO usuario_id FROM usuarios ORDER BY random() LIMIT 1;
        
        -- Generar un monto de venta
        monto_val := trunc(random() * (30000000 - 5000000) + 5000000);
        
        -- Fecha de venta aleatoria en últimos 5 años
        fecha_venta := NOW() - (trunc(random() * 1825) || ' days')::interval;
        
        INSERT INTO "Hechos_ventas" (
            id_concesionaria,
            id_usuario,
            id_auto,
            monto,
            fecha_venta,
            id_modelo,
            id_ciudad,
            id_region,
            id_comuna
        ) VALUES (
            concesionaria_id,
            usuario_id,
            auto_record.patente,
            monto_val,
            fecha_venta,
            auto_record.id_modelo,
            ciudad_id,
            region_id,
            comuna_id
        );
    END LOOP;
END $$;

