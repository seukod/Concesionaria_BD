def run_etl():
    print("Iniciando proceso ETL...")

    from extract import (
        extract_modelos, extract_autos, extract_concesionarias, extract_usuarios,
        extract_region, extract_comunas, extract_ciudades,
        extract_hechos_compras, extract_hechos_ventas
    )
    from transform import transform_data
    from load import (
        load_modelos, load_autos, load_concesionarias, load_usuarios,
        load_region, load_comunas, load_ciudades,
        load_hechos_compras, load_hechos_ventas
    )

    # MODELOS
    modelos = extract_modelos()
    if modelos:
        load_modelos(transform_data(modelos))
        print(f"Se cargaron {len(modelos)} modelos en analisis.modelos.")

    # AUTOS
    autos = extract_autos()
    if autos:
        load_autos(transform_data(autos))
        print(f"Se cargaron {len(autos)} autos en analisis.autos.")

    # CONCESIONARIAS
    concesionarias = extract_concesionarias()
    if concesionarias:
        load_concesionarias(transform_data(concesionarias))
        print(f"Se cargaron {len(concesionarias)} concesionarias en analisis.concesionarias.")

    # USUARIOS
    usuarios = extract_usuarios()
    if usuarios:
        load_usuarios(transform_data(usuarios))
        print(f"Se cargaron {len(usuarios)} usuarios en analisis.usuarios.")

    # REGION
    regiones = extract_region()
    if regiones:
        load_region(transform_data(regiones))
        print(f"Se cargaron {len(regiones)} regiones en analisis.region.")

    # COMUNAS
    comunas = extract_comunas()
    if comunas:
        load_comunas(transform_data(comunas))
        print(f"Se cargaron {len(comunas)} comunas en analisis.comunas.")

    # CIUDADES
    ciudades = extract_ciudades()
    if ciudades:
        load_ciudades(transform_data(ciudades))
        print(f"Se cargaron {len(ciudades)} ciudades en analisis.ciudades.")

    # HECHOS_COMPRAS
    hechos_compras = extract_hechos_compras()
    if hechos_compras:
        load_hechos_compras(transform_data(hechos_compras))
        print(f"Se cargaron {len(hechos_compras)} filas en analisis.Hechos_compras.")

    # HECHOS_VENTAS
    hechos_ventas = extract_hechos_ventas()
    if hechos_ventas:
        load_hechos_ventas(transform_data(hechos_ventas))
        print(f"Se cargaron {len(hechos_ventas)} filas en analisis.Hechos_ventas.")

    print("ETL finalizada.")