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

def main():
    parser = argparse.ArgumentParser(description="Consulta base de datos por año")
    parser.add_argument("anio", help="Año para filtrar datos, formato YYYY")
    args = parser.parse_args()

    conn = conectar()

    print(f"Ventas por mes para el año {args.anio}:")
    ventas = ventas_por_mes(conn, args.anio)
    for anomes, count in ventas:
        print(f"{anomes}: {count}")

    print(f"\nCompras, ventas y diferencia para el año {args.anio}:")
    datos = compras_ventas_diferencia(conn, args.anio)
    for anomes, monto_ventas, monto_compras, diferencia in datos:
        print(f"{anomes}: Ventas={monto_ventas}, Compras={monto_compras}, Diferencia={diferencia}")

    conn.close()

if __name__ == "__main__":
    main()
