import psycopg2
import argparse

def conectar():
    return psycopg2.connect(
        host="aws-0-sa-east-1.pooler.supabase.com",
        password="0NzSHHo6Ee9Hl4BI",
        port="5432",
        database="tabladehechos",
        user="postgres.qdxsvygmfuqrrcaisqvw"
    )

def ventas_por_mes(conn, anio):
    query = """
    SELECT TO_CHAR(hv.fecha_venta, 'YYYY-MM') AS anomes,
           COUNT(*) AS count
    FROM "Hechos_ventas" hv 
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY TO_CHAR(hv.fecha_venta, 'YYYY-MM')
    ORDER BY anomes;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        return cursor.fetchall()

def compras_ventas_diferencia(conn, anio):
    query = """
    SELECT COALESCE(compraAnomes, VentaAnomes) AS anomes,
           COALESCE(ventasmes.monto_ventas, 0) AS monto_ventas,
           COALESCE(comprames.monto_compras, 0) AS monto_compras,
           COALESCE(ventasmes.monto_ventas, 0) - COALESCE(comprames.monto_compras, 0) AS diferencia
    FROM 
    (
        SELECT TO_CHAR(hc.fecha_compra, 'YYYY-MM') AS compraAnomes,
               SUM(hc.monto) AS monto_compras
        FROM "Hechos_compras" hc
        WHERE TO_CHAR(hc.fecha_compra, 'YYYY') = %s
        GROUP BY compraAnomes
        ORDER BY compraAnomes
    ) AS comprames
    FULL JOIN
    (
        SELECT TO_CHAR(hv.fecha_venta, 'YYYY-MM') AS VentaAnomes,
               SUM(hv.monto) AS monto_ventas
        FROM "Hechos_ventas" hv
        WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
        GROUP BY VentaAnomes
        ORDER BY VentaAnomes
    ) AS ventasmes
    ON comprames.compraanomes = ventasmes.VentaAnomes;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio, anio))
        return cursor.fetchall()
    
def top_5_modelos_mas_vendidos(conn, anio):
    query = """
    SELECT m.nombre_modelo,
           COUNT(*) AS cantidad_vendida
    FROM "Hechos_ventas" hv
    JOIN modelos m ON hv.id_modelo = m.id_modelo
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY m.nombre_modelo
    ORDER BY cantidad_vendida DESC
    LIMIT 5;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        return cursor.fetchall()


def modelo_mas_vendido_por_region(conn, anio):
    query = """
    SELECT id_region, nombre_modelo, cantidad_vendida
    FROM (
        SELECT hv.id_region,
               m.nombre_modelo,
               COUNT(*) AS cantidad_vendida,
               RANK() OVER (PARTITION BY hv.id_region ORDER BY COUNT(*) DESC) AS ranking
        FROM "Hechos_ventas" hv
        JOIN modelos m ON hv.id_modelo = m.id_modelo
        WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
        GROUP BY hv.id_region, m.nombre_modelo
    ) ranked
    WHERE ranked.ranking = 1;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        return cursor.fetchall()


def comparacion_compras_vs_ventas_por_region(conn, anio):
    query = """
    SELECT COALESCE(vc.id_region, cc.id_region) AS id_region,
           COALESCE(vc.vendidos, 0) AS autos_vendidos,
           COALESCE(cc.comprados, 0) AS autos_comprados
    FROM (
        SELECT id_region, COUNT(*) AS vendidos
        FROM "Hechos_ventas"
        WHERE TO_CHAR(fecha_venta, 'YYYY') = %s
        GROUP BY id_region
    ) vc
    FULL OUTER JOIN (
        SELECT id_region, COUNT(*) AS comprados
        FROM "Hechos_compras"
        WHERE TO_CHAR(fecha_compra, 'YYYY') = %s
        GROUP BY id_region
    ) cc ON vc.id_region = cc.id_region
    ORDER BY id_region;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio, anio))
        return cursor.fetchall()


def promedio_precio_venta_por_marca(conn, anio):
    query = """
    SELECT m.marca,
           AVG(a.precio) AS promedio_precio_venta
    FROM "Hechos_ventas" hv
    JOIN autos a ON hv.id_auto = a.patente
    JOIN modelos m ON hv.id_modelo = m.id_modelo
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY m.marca
    ORDER BY promedio_precio_venta DESC;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        return cursor.fetchall()


def main():
    parser = argparse.ArgumentParser(description="Consulta base de datos por año")
    parser.add_argument("anio", help="Año para filtrar datos, formato YYYY")
    args = parser.parse_args()

    conn = conectar()

    print(f"\nVentas por mes para el año {args.anio}:")
    ventas = ventas_por_mes(conn, args.anio)
    for anomes, count in ventas:
        print(f"{anomes}: {count}")

    print(f"\nCompras, ventas y diferencia para el año {args.anio}:")
    datos = compras_ventas_diferencia(conn, args.anio)
    for anomes, monto_ventas, monto_compras, diferencia in datos:
        print(f"{anomes}: Ventas={monto_ventas}, Compras={monto_compras}, Diferencia={diferencia}")

    print(f"\nTop 5 modelos más vendidos en {args.anio}:")
    top_modelos = top_5_modelos_mas_vendidos(conn, args.anio)
    for nombre_modelo, cantidad in top_modelos:
        print(f"{nombre_modelo}: {cantidad} ventas")

    print(f"\nModelo más vendido por región en {args.anio}:")
    modelos_region = modelo_mas_vendido_por_region(conn, args.anio)
    for id_region, modelo, cantidad in modelos_region:
        print(f"Región {id_region}: {modelo} ({cantidad} ventas)")

    print(f"\nComparación de autos comprados vs vendidos por región en {args.anio}:")
    comparacion = comparacion_compras_vs_ventas_por_region(conn, args.anio)
    for id_region, vendidos, comprados in comparacion:
        print(f"Región {id_region}: Vendidos={vendidos}, Comprados={comprados}")

    print(f"\nPromedio de precio de venta por marca en {args.anio}:")
    precios = promedio_precio_venta_por_marca(conn, args.anio)
    for marca, promedio in precios:
        print(f"{marca}: ${promedio:.2f}")

    conn.close()

    

if __name__ == "__main__":
    main()
