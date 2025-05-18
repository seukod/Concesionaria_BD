import psycopg2
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import textwrap
from matplotlib.ticker import FuncFormatter
import calendar
from datetime import datetime

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
        resultados = cursor.fetchall()

    # Mostrar en consola
    for anomes, count in resultados:
        print(f"{anomes}: {count}")

    # Si hay resultados, generar gráfico
    if resultados:
        anomes_raw = [r[0] for r in resultados]
        cantidad = [r[1] for r in resultados]

        # Convertir "YYYY-MM" a "Mes Año"
        anomes = []
        for fecha in anomes_raw:
            try:
                dt = datetime.strptime(fecha, "%Y-%m")
                nombre_mes = calendar.month_name[dt.month].capitalize()
                anomes.append(f"{nombre_mes} {dt.year}")
            except:
                anomes.append(fecha)  # fallback si algo falla

        plt.figure(figsize=(10, 5))
        sns.barplot(x=anomes, y=cantidad, palette="Blues_d")

        plt.title(f'Ventas por mes - {anio}')
        plt.xticks(rotation=45)
        plt.ylabel('Cantidad de ventas')
        plt.xlabel('Mes')
        plt.tight_layout()

        # Crear carpeta si no existe
        output_dir = "graficos"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/ventas_por_mes_{anio}.png"

        plt.savefig(filename)
        plt.show()
        plt.close()

        print(f"\n Gráfico guardado como: {filename}")
        print("Guardando gráfico en:", os.path.abspath(output_dir))
    else:
        print("\n No se encontraron resultados para ese año.")

    return resultados

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
        datos = cursor.fetchall()
    
    # Procesar los datos
    meses = [fila[0] for fila in datos]
    ventas = [fila[1] for fila in datos]
    compras = [fila[2] for fila in datos]
    diferencias = [fila[3] for fila in datos]

    # ---------- GRÁFICO DE BARRAS AGRUPADAS ----------
    x = np.arange(len(meses))
    ancho = 0.25

    plt.figure(figsize=(14, 6))
    plt.bar(x - ancho, ventas, width=ancho, label='Ventas', color='green')
    plt.bar(x, compras, width=ancho, label='Compras', color='blue')
    plt.bar(x + ancho, diferencias, width=ancho, label='Diferencia', color='red')

    plt.title(f'Comparación mensual de Compras, Ventas y Diferencia - {anio}')
    plt.xlabel('Mes')
    plt.ylabel('Monto en CLP')
    plt.xticks(x, meses, rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f'comparacion_barras_{anio}.png')
    plt.show()

    return datos
    
def top_10_modelos_mas_vendidos(conn, anio):
    query = """
    SELECT m.nombre_modelo,
           COUNT(*) AS cantidad_vendida
    FROM "Hechos_ventas" hv
    JOIN modelos m ON hv.id_modelo = m.id_modelo
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY m.nombre_modelo
    ORDER BY cantidad_vendida DESC
    LIMIT 10;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    # Extraer datos
    modelos = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    # Graficar
    plt.figure(figsize=(10, 6))
    barras = plt.barh(modelos, cantidades, color='skyblue')
    plt.xlabel('Cantidad de unidades vendidas')
    plt.ylabel('Modelos')
    plt.title(f'Top 10 Modelos más Vendidos - {anio}')
    plt.gca().invert_yaxis()  # El más vendido arriba

    for barra in barras:
        ancho = barra.get_width()
        plt.text(ancho + 0.1, barra.get_y() + barra.get_height()/2,
                 str(int(ancho)), va='center')

    plt.tight_layout()
    plt.show()

    return resultados


def modelo_mas_vendido_por_region(conn, anio):
    query = """
    SELECT r.nombre_region, ranked.nombre_modelo, ranked.cantidad_vendida
    FROM (
        SELECT hv.id_region,
               m.nombre_modelo,
               COUNT(*) AS cantidad_vendida,
               ROW_NUMBER() OVER (PARTITION BY hv.id_region ORDER BY COUNT(*) DESC) AS fila
        FROM "Hechos_ventas" hv
        JOIN modelos m ON hv.id_modelo = m.id_modelo
        WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
        GROUP BY hv.id_region, m.nombre_modelo
    ) ranked
    JOIN region r ON ranked.id_region = r.id_region
    WHERE ranked.fila = 1;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    # Ajustar nombres largos con saltos de línea
    def wrap_label(label, width=15):
        return "\n".join(textwrap.wrap(label, width))

    regiones = [wrap_label(fila[0]) for fila in resultados]
    modelos = [fila[1] for fila in resultados]
    cantidades = [fila[2] for fila in resultados]
    etiquetas = [f"{modelo} ({cant} ventas)" for modelo, cant in zip(modelos, cantidades)]

    # Gráfico
    plt.figure(figsize=(12, 6))
    barras = plt.bar(regiones, cantidades, color='mediumseagreen')
    plt.xticks(rotation=0, fontsize=9)
    plt.ylabel('Unidades vendidas')
    plt.title(f'Modelo más vendido por Región - {anio}')

    # Ajustar el espacio superior
    plt.ylim(0, max(cantidades) + 1.5)

    for barra, etiqueta in zip(barras, etiquetas):
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2,
                 altura + 0.1,
                 etiqueta,
                 ha='center', va='bottom',
                 fontsize=8, rotation=0,
                 wrap=True)

    plt.tight_layout()
    plt.show()

    return resultados




def comparacion_compras_vs_ventas_por_region(conn, anio):
    query = """
    SELECT r.nombre_region,
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
    JOIN region r ON r.id_region = COALESCE(vc.id_region, cc.id_region)
    ORDER BY r.id_region;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio, anio))
        resultados = cursor.fetchall()

    if resultados:
        # Función para envolver texto largo
        def wrap_label(label, width=15):
            return "\n".join(textwrap.wrap(label, width))

        regiones = [wrap_label(r[0]) for r in resultados]
        vendidos = [r[1] for r in resultados]
        comprados = [r[2] for r in resultados]

        x = range(len(regiones))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar([i - width/2 for i in x], vendidos, width=width, label='Vendidos', color='steelblue')
        plt.bar([i + width/2 for i in x], comprados, width=width, label='Comprados', color='darkorange')

        plt.xticks(x, regiones, rotation=0, fontsize=9)
        plt.title(f'Comparación de autos comprados vs vendidos por región - {anio}')
        plt.xlabel('Región')
        plt.ylabel('Cantidad')
        plt.legend()
        plt.tight_layout()

        output_dir = "graficos"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/comparacion_compras_vs_ventas_por_region_{anio}.png"
        plt.savefig(filename)
        plt.show()
        plt.close()
        print(f"\nGráfico guardado como: {filename}")
        print("Guardando gráfico en:", os.path.abspath(output_dir))
    else:
        print("\nNo se encontraron resultados para ese año.")

    return resultados


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
        resultados = cursor.fetchall()

    # Mostrar resultados en consola con formato
    for marca, promedio in resultados:
        print(f"{marca}: ${promedio:,.0f} CLP")

    if resultados:
        marcas = [r[0] for r in resultados]
        promedios = [r[1] for r in resultados]
        etiquetas = [f"${p:,.0f} CLP" for p in promedios]

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=promedios, y=marcas, palette="coolwarm")

        plt.title(f'Promedio de precio de venta por marca - {anio}')
        plt.xlabel('Precio promedio (CLP)')
        plt.ylabel('Marca')

        # Ajustar límites del eje x
        max_valor = max(promedios)
        plt.xlim(0, max_valor * 1.1)

        # Formatear eje X en miles/millones con CLP
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

        # Añadir etiquetas de precio
        for i, (valor, etiqueta) in enumerate(zip(promedios, etiquetas)):
            ax.text(valor * 0.98, i, etiqueta,
                    va='center', ha='right', fontsize=9,
                    color='black', weight='bold')

        plt.tight_layout()

        output_dir = "graficos"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/promedio_precio_venta_pormarca{anio}.png"
        plt.savefig(filename)
        plt.show()
        plt.close()
        print(f"\nGráfico guardado como: {filename}")
        print("Guardando gráfico en:", os.path.abspath(output_dir))
    else:
        print("\nNo se encontraron resultados para ese año.")

    return resultados


def main():
    parser = argparse.ArgumentParser(description="Consulta base de datos por año")
    parser.add_argument("anio", help="Año para filtrar datos, formato YYYY")
    args = parser.parse_args()
    
    conn = conectar()
    #LISTO
    """print(f"\nVentas por mes para el año {args.anio}:")
    ventas = ventas_por_mes(conn, args.anio)
    for anomes, count in ventas:
        print(f"{anomes}: {count}")"""
    #Pendiente
    print(f"\nCompras, ventas y diferencia para el año {args.anio}:")
    datos = compras_ventas_diferencia(conn, args.anio)
    for anomes, monto_ventas, monto_compras, diferencia in datos:
        print(f"{anomes}: Ventas={monto_ventas}, Compras={monto_compras}, Diferencia={diferencia}")
    #LISTO
    """print(f"\nTop 10 modelos más vendidos en {args.anio}:")
    top_modelos = top_10_modelos_mas_vendidos(conn, args.anio)
    for nombre_modelo, cantidad in top_modelos:
        print(f"{nombre_modelo}: {cantidad} ventas")"""
    #LISTO
    """print(f"\nModelo más vendido por región en {args.anio}:")
    modelos_region = modelo_mas_vendido_por_region(conn, args.anio)
    for id_region, modelo, cantidad in modelos_region:
        print(f"Región {id_region}: {modelo} ({cantidad} ventas)")"""
    #LISTO
    """print(f"\nComparación de autos comprados vs vendidos por región en {args.anio}:")
    comparacion = comparacion_compras_vs_ventas_por_region(conn, args.anio)
    for id_region, vendidos, comprados in comparacion:
        print(f"Región {id_region}: Vendidos={vendidos}, Comprados={comprados}")"""
    #LISTO
    """print(f"\nPromedio de precio de venta por marca en {args.anio}:")
    precios = promedio_precio_venta_por_marca(conn, args.anio)
    for marca, promedio in precios:
        print(f"{marca}: ${promedio:.2f}")"""

    conn.close()

    

if __name__ == "__main__":
    main()