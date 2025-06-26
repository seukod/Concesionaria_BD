CREATE SCHEMA IF NOT EXISTS transaccional;
SET search_path TO transaccional;

-- Borrar datos en orden correcto (dependientes primero)
TRUNCATE TABLE 
    ventas,
    transferencias,
    compras,
    autos,
    modelos,
    concesionarias,
    ciudad,
    comuna,
    region,
    usuarios
RESTART IDENTITY CASCADE;

--REGIO------

INSERT INTO region (id_region, nombre_region) VALUES
  (1, 'Región de Arica y Parinacota'),
  (2, 'Región de Tarapacá'),
  (3, 'Región de Antofagasta'),
  (4, 'Región de Atacama'),
  (5, 'Región de Coquimbo'),
  (6, 'Región de Valparaíso'),
  (7, 'Región Metropolitana de Santiago'),
  (8, 'Región del Libertador General Bernardo OHiggins'),
  (9, 'Región del Maule'),
  (10, 'Región de Ñuble'),  -- ¡La que faltaba!
  (11, 'Región del Biobío'),
  (12, 'Región de La Araucanía'),
  (13, 'Región de Los Ríos'),
  (14, 'Región de Los Lagos'),
  (15, 'Región de Aysén del General Carlos Ibáñez del Campo'),
  (16, 'Región de Magallanes y de la Antártica Chilena');
  
  --COMUNA--
  
INSERT INTO comuna (id_comuna, id_region_perteneciente, nombre_comuna) VALUES
  (1, 1, 'Arica'),
  (2, 1, 'Putre'),
  (3, 1, 'Camarones'),
  (4, 2, 'Iquique'),
  (5, 2, 'Alto Hospicio'),
  (6, 2, 'Pozo Almonte'),
  (7, 3, 'Antofagasta'),
  (8, 3, 'Calama'),
  (9, 3, 'Tocopilla'),
  (10, 4, 'Copiapó'),
  (11, 4, 'Vallenar'),
  (12, 4, 'Chañaral'),
  (13, 5, 'La Serena'),
  (14, 5, 'Coquimbo'),
  (15, 5, 'Ovalle'),
  (16, 6, 'Valparaíso'),
  (17, 6, 'Viña del Mar'),
  (18, 6, 'Quilpué'),
  (43, 7, 'Santiago'),
  (44, 7, 'Puente Alto'),
  (45, 7, 'Maipú'),
  (19, 8, 'Rancagua'),
  (20, 8, 'San Fernando'),
  (21, 8, 'Rengo'),
  (22, 9, 'Talca'),
  (23, 9, 'Curicó'),
  (24, 9, 'Linares'),
  (46, 10, 'Chillán'),
  (47, 10, 'San Carlos'),
  (48, 10, 'Bulnes'),
  (25, 11, 'Concepción'),
  (26, 11, 'Talcahuano'),
  (27, 11, 'Los Ángeles'),
  (28, 12, 'Temuco'),
  (29, 12, 'Villarrica'),
  (30, 12, 'Angol'),
  (31, 13, 'Valdivia'),
  (32, 13, 'La Unión'),
  (33, 13, 'Río Bueno'),
  (34, 14, 'Puerto Montt'),
  (35, 14, 'Osorno'),
  (36, 14, 'Castro'),
  (37, 15, 'Coyhaique'),
  (38, 15, 'Puerto Aysén'),
  (39, 15, 'Chile Chico'),
  (40, 16, 'Punta Arenas'),
  (41, 16, 'Puerto Natales'),
  (42, 16, 'Porvenir');
  
  --CIUDAD--

INSERT INTO ciudad (id_ciudad, id_comuna_perteneciente, nombre_ciudad) VALUES
  (1, 1, 'Arica'),
  (2, 2, 'Putre'),
  (3, 3, 'Camarones'),
  (4, 4, 'Iquique'),
  (5, 5, 'Alto Hospicio'),
  (6, 6, 'Pozo Almonte'),
  (7, 7, 'Antofagasta'),
  (8, 8, 'Calama'),
  (9, 9, 'Tocopilla'),
  (10, 10, 'Copiapó'),
  (11, 11, 'Vallenar'),
  (12, 12, 'Chañaral'),
  (13, 13, 'La Serena'),
  (14, 14, 'Coquimbo'),
  (15, 15, 'Ovalle'),
  (16, 16, 'Valparaíso'),
  (17, 17, 'Viña del Mar'),
  (18, 18, 'Quilpué'),
  (19, 19, 'Rancagua'),
  (20, 20, 'San Fernando'),
  (21, 21, 'Rengo'),
  (22, 22, 'Talca'),
  (23, 23, 'Curicó'),
  (24, 24, 'Linares'),
  (25, 25, 'Concepción'),
  (26, 26, 'Talcahuano'),
  (27, 27, 'Los Ángeles'),
  (28, 28, 'Temuco'),
  (29, 29, 'Villarrica'),
  (30, 30, 'Angol'),
  (31, 31, 'Valdivia'),
  (32, 32, 'La Unión'),
  (33, 33, 'Río Bueno'),
  (34, 34, 'Puerto Montt'),
  (35, 35, 'Osorno'),
  (36, 36, 'Castro'),
  (37, 37, 'Coyhaique'),
  (38, 38, 'Puerto Aysén'),
  (39, 39, 'Chile Chico'),
  (40, 40, 'Punta Arenas'),
  (41, 41, 'Puerto Natales'),
  (42, 42, 'Porvenir'),
  (43, 43, 'Santiago'),
  (44, 44, 'Puente Alto'),
  (45, 45, 'Maipú'),
  (46, 46, 'Chillán'),
  (47, 47, 'San Carlos'),
  (48, 48, 'Bulnes');
  
--CONCESIONARIAS--

INSERT INTO concesionarias (id_ciudad_concesionaria, direccion) VALUES
(1, 'Av. Santa María 123'),
(1, 'Calle San Marcos 456'),
(2, 'Av. Libertad 789'),
(2, 'Pasaje Andino 321'),
(3, 'Ruta Costera 654'),
(3, 'Calle Los Pescadores 987'),
(4, 'Av. Arturo Prat 555'),
(4, 'Balmaceda 222'),
(5, 'Av. La Pampa 777'),
(5, 'Los Tamarugos 333'),
(6, 'Av. Tarapacá 111'),
(6, 'Ovalle 888'),
(7, 'Av. Argentina 444'),
(7, 'Latorre 999'),
(8, 'Av. Granaderos 666'),
(8, 'Sotomayor 222'),
(9, 'Av. Circunvalación 777'),
(9, 'Serrano 333'),
(10, 'Av. Los Carrera 123'),
(10, 'Atacama 456'),
(11, 'Av. Brasil 789'),
(11, 'Esmeralda 321'),
(12, 'Av. Diego de Almeyda 654'),
(12, 'Merced 987'),
(13, 'Av. Francisco de Aguirre 555'),
(13, 'Balmaceda 222'),
(14, 'Av. Costanera 777'),
(14, 'O Higgins 333'),
(15, 'Av. Libertad 111'),
(15, 'Vicuña 888'),
(16, 'Av. Argentina 444'),
(16, 'Errázuriz 999'),
(17, 'Av. Libertad 666'),
(17, 'Quillota 222'),
(18, 'Av. Freire 777'),
(18, 'Condell 333'),
(19, 'Av. Millán 123'),
(19, 'Cachapoal 456'),
(20, 'Av. Manso de Velasco 789'),
(20, 'Colchagua 321'),
(21, 'Av. Bisquertt 654'),
(21, 'Carampangue 987'),
(22, 'Av. San Miguel 555'),
(22, '1 Poniente 222'),
(23, 'Av. Manso de Velasco 777'),
(23, 'Peña 333'),
(24, 'Av. Valentín Letelier 111'),
(24, 'Arturo Prat 888'),
(25, 'Av. Arturo Prat 444'),
(25, 'Barros Arana 999'),
(26, 'Av. Colón 666'),
(26, 'Aníbal Pinto 222'),
(27, 'Av. Ricardo Vicuña 777'),
(27, 'Villagrán 333'),
(28, 'Av. Alemania 123'),
(28, 'Caupolicán 456'),
(29, 'Av. Pedro de Valdivia 789'),
(29, 'Bernardo O Higgins 321'),
(30, 'Av. Pinto 654'),
(30, 'Lautaro 987'),
(31, 'Av. Picarte 555'),
(31, 'Yungay 222'),
(32, 'Av. Presidente Ibáñez 777'),
(32, 'O Higgins 333'),
(33, 'Av. Carlos Condell 111'),
(33, 'Arturo Prat 888'),
(34, 'Av. Diego Portales 444'),
(34, 'Urmeneta 999'),
(35, 'Av. Mackenna 666'),
(35, 'Eleuterio Ramírez 222'),
(36, 'Av. Pedro Montt 777'),
(36, 'Esmeralda 333'),
(37, 'Av. General Baquedano 123'),
(37, 'Horn 456'),
(38, 'Av. Presidente Ibáñez 789'),
(38, 'Sargento Aldea 321'),
(39, 'Av. O Higgins 654'),
(39, 'Balmaceda 987'),
(40, 'Av. Colón 555'),
(40, 'Bories 222'),
(41, 'Av. Santiago Bueras 777'),
(41, 'Bulnes 333'),
(42, 'Av. Manuel Señoret 111'),
(42, 'Philippi 888'),
(43, 'Av. Providencia 444'),
(43, 'Alameda 999'),
(44, 'Av. Concha y Toro 666'),
(44, 'Eyzaguirre 222'),
(45, 'Av. Pajaritos 777'),
(45, '5 de Abril 333'),
(46, 'Av. Argentina 123'),
(46, 'O Higgins 456'),
(47, 'Av. O Higgins 789'),
(47, 'Arturo Prat 321'),
(48, 'Av. Bernardo O Higgins 654'),
(48, 'Serrano 987');

--MODELOS--

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

-- AUTOS

DO $$
DECLARE
    i INTEGER := 0;
    letras TEXT;
    digitos TEXT;
    patente_auto TEXT;
    modelo_id INTEGER;
    limite INTEGER := 2000; -- Ahora 2000 autos
BEGIN
    WHILE i < limite LOOP
        -- Generar patente tipo AAAA01
        letras := chr(trunc(65 + random() * 26)::int) ||
                  chr(trunc(65 + random() * 26)::int) ||
                  chr(trunc(65 + random() * 26)::int) ||
                  chr(trunc(65 + random() * 26)::int);
        digitos := lpad(trunc(random() * 99 + 1)::text, 2, '0');
        patente_auto := letras || digitos;

        -- Verificar si ya existe la patente
        IF NOT EXISTS (SELECT 1 FROM autos WHERE patente = patente_auto) THEN
            -- Elegir modelo al azar
            SELECT id_modelo INTO modelo_id FROM modelos ORDER BY random() LIMIT 1;

            -- Insertar el auto
            INSERT INTO autos (patente, precio, auto_prueba, disponible, fecha_llegada, kilometraje, modelo)
            VALUES (
                patente_auto,
                trunc(random() * (30000000 - 5000000) + 5000000),
                (random() < 0.3),
                (random() < 0.8),
                NOW() - (trunc(random() * 1825) || ' days')::interval,
                trunc(random() * 200000),
                modelo_id
            );

            i := i + 1;
        END IF;
    END LOOP;
END $$;


--USUARIOS--

DO $$
DECLARE
    i INTEGER := 0;
    rut_generado INTEGER;
    nombres TEXT[] := ARRAY['Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Carla', 'José', 'Camila', 'Felipe', 'Sofía', 'Diego', 'Isabel', 'Jorge', 'Lucía', 'Andrés', 'Paula', 'Ricardo', 'Claudia', 'Tomás', 'Marta', 'Sebastián', 'Valentina', 'Francisco', 'Antonia', 'Matías', 'Fernanda', 'Cristóbal', 'Javiera', 'Vicente', 'Daniela', 'Benjamín', 'Josefa', 'Martina', 'Agustín', 'Emilia', 'Maximiliano', 'Trinidad', 'Gabriel', 'Florencia', 'Samuel', 'Amanda'];
    apellidos TEXT[] := ARRAY['González', 'Rodríguez', 'Muñoz', 'Pérez', 'Soto', 'Rojas', 'Contreras', 'Silva', 'Martínez', 'Torres', 'Flores', 'López', 'Castillo', 'Vargas', 'Cruz', 'Molina', 'Fuentes', 'Vega', 'Orellana', 'Herrera', 'Reyes', 'Morales', 'Gutiérrez', 'Pizarro', 'Cáceres', 'Navarro', 'Salazar', 'Campos', 'Araya', 'Miranda', 'Valenzuela', 'Tapia', 'Ruiz', 'Saavedra', 'Carrasco', 'Bravo', 'Parra', 'Cortés', 'Gallardo', 'Acosta', 'Espinoza'];
    profesiones TEXT[] := ARRAY['Ingeniero', 'Profesor', 'Médico', 'Abogado', 'Arquitecto', 'Contador', 'Periodista', 'Enfermero', 'Diseñador', 'Técnico', 'Administrativo', 'Psicólogo', 'Electrónico', 'Veterinario', 'Químico', 'Odontólogo', 'Kinesiólogo', 'Fonoaudiólogo', 'Nutricionista', 'Farmacéutico'];
    limite INTEGER := 2000; -- Ahora 2000 usuarios
BEGIN
    WHILE i < limite LOOP
        rut_generado := (random() * (25000000 - 1000000) + 1000000)::int;

        -- Verificar si ya existe ese rut
        PERFORM 1 FROM usuarios WHERE rut = rut_generado;

        IF NOT FOUND THEN
            INSERT INTO usuarios (rut, nombre, apellido, profesion, socio)
            VALUES (
                rut_generado,
                nombres[trunc(random() * array_length(nombres, 1) + 1)::int],
                apellidos[trunc(random() * array_length(apellidos, 1) + 1)::int],
                profesiones[trunc(random() * array_length(profesiones, 1) + 1)::int],
                (random() < 0.3)
            );
            i := i + 1;
        END IF;
    END LOOP;
END $$;


--COMPRA--

DO $$
DECLARE
    auto RECORD;
    concesionaria_id INTEGER;
    fecha_compra TIMESTAMP;
    meses_desde_hoy INTEGER := 36;
    mes_offset INTEGER;
    dia_del_mes INTEGER;
    i INTEGER := 0;
    limite INTEGER := 2000; -- Ahora 2000 compras
BEGIN
    -- Recorremos todos los autos que aún no han sido comprados
    FOR auto IN
        SELECT a.patente, a.precio
        FROM autos a
        WHERE NOT EXISTS (
            SELECT 1 FROM compras c WHERE c.id_auto = a.patente
        )
        ORDER BY random()
    LOOP
        -- Salir si se generan más de 2000 compras
        EXIT WHEN i >= limite;

        -- Elegir concesionaria aleatoria
        SELECT id_concesionarias INTO concesionaria_id
        FROM concesionarias
        ORDER BY random()
        LIMIT 1;

        -- Distribuir fecha en los últimos 36 meses
        mes_offset := (i / 500)::int;  -- cada 500 compras, cambia el mes
        dia_del_mes := trunc(random() * 28 + 1);

        fecha_compra := date_trunc('month', CURRENT_DATE) - (mes_offset || ' months')::interval
                        + (dia_del_mes || ' days')::interval;

        -- Insertar la compra con el mismo precio del auto
        INSERT INTO compras (
            fecha_compra,
            monto,
            concesionaria,
            id_auto
        ) VALUES (
            fecha_compra,
            auto.precio,
            concesionaria_id,
            auto.patente
        );

        i := i + 1;
    END LOOP;
END $$;


--Venta--

DO $$
DECLARE
    i INTEGER := 0;
    venta RECORD;
    usuario RECORD;
    precio_base FLOAT;
    monto_final FLOAT;
    fecha_venta TIMESTAMP;
    mes_offset INTEGER;
    dia_del_mes INTEGER;
    limite INTEGER := 2000; -- Ahora 2000 ventas
BEGIN
    -- Recorre autos que fueron comprados, evita autos repetidos
    FOR venta IN
        SELECT a.patente, a.precio
        FROM autos a
        WHERE a.patente IN (SELECT id_auto FROM compras)
        ORDER BY random()
    LOOP
        EXIT WHEN i >= limite;

        -- Elegir usuario aleatorio
        SELECT rut, socio INTO usuario
        FROM usuarios
        ORDER BY random()
        LIMIT 1;

        -- Calcular monto de venta: 15% más del precio del auto
        precio_base := venta.precio * 1.15;

        -- Si es socio, aplicar 5% de descuento
        IF usuario.socio THEN
            monto_final := precio_base * 0.95;
        ELSE
            monto_final := precio_base;
        END IF;

        -- Obtener concesionaria que vendió el auto (puede ser aleatoria también)
        -- o relacionada con la compra si se desea ser más estricto
        -- Aquí usamos una al azar para simplificar
        DECLARE
            concesionaria_id INTEGER;
        BEGIN
            SELECT id_concesionarias INTO concesionaria_id
            FROM concesionarias
            ORDER BY random()
            LIMIT 1;

            -- Fecha distribuida entre últimos 3 años
            mes_offset := (i / 500)::int; -- cada 500 ventas cambia el mes
            dia_del_mes := trunc(random() * 28 + 1);
            fecha_venta := date_trunc('month', CURRENT_DATE) - (mes_offset || ' months')::interval + (dia_del_mes || ' days')::interval;

            -- Insertar la venta
            INSERT INTO ventas (
                id_concesionaria,
                id_usuario,
                id_auto,
                monto,
                fecha_venta
            ) VALUES (
                concesionaria_id,
                usuario.rut,
                venta.patente,
                monto_final,
                fecha_venta
            );
        END;

        i := i + 1;
    END LOOP;
END $$;

--TRANSFERENCIAS--
DO $$
DECLARE
    auto RECORD;
    concesionarias_ids INTEGER[];
    nueva_concesionaria INTEGER;
    comentario_text TEXT[] := ARRAY[
        'Rotación de stock',
        'Mejor demanda en otra región',
        'Poca rotación en ubicación actual',
        'Redistribución logística',
        'A solicitud del gerente regional'
    ];
BEGIN
    -- Obtener IDs de todas las concesionarias
    SELECT array_agg(id_concesionarias) INTO concesionarias_ids FROM concesionarias;

    FOR auto IN
        SELECT patente, fecha_llegada, disponible
        FROM autos
        WHERE fecha_llegada < NOW() - INTERVAL '2 years' AND disponible = TRUE
    LOOP
        -- Elegir concesionaria diferente al azar
        LOOP
            nueva_concesionaria := concesionarias_ids[ceil(random() * array_length(concesionarias_ids, 1))::int];
            EXIT WHEN nueva_concesionaria IS DISTINCT FROM (
                SELECT c.id_concesionarias
                FROM compras cp
                JOIN concesionarias c ON c.id_concesionarias = cp.concesionaria
                WHERE cp.id_auto = auto.patente
                ORDER BY cp.fecha_compra DESC
                LIMIT 1
            );
        END LOOP;

        -- Insertar transferencia
        INSERT INTO transferencias (id_transferencia, desde, hasta, id_auto, comentario)
        VALUES (
            DEFAULT,
            (SELECT concesionaria FROM compras WHERE id_auto = auto.patente ORDER BY fecha_compra DESC LIMIT 1),
            nueva_concesionaria,
            auto.patente,
            comentario_text[ceil(random() * array_length(comentario_text, 1))::int]
        );
    END LOOP;
END $$;





