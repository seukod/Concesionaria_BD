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
import matplotlib.ticker as mtick

def conectar():
    return psycopg2.connect(
        host="localhost",
        password="5540",
        port="5432",
        database="postgres",
        user="postgres"
    )

def ventas_por_mes(conn, anio):
    query = """
    SELECT TO_CHAR(hv.fecha_venta, 'YYYY-MM') AS anomes,
           COUNT(*) AS count
    FROM analisis.hechos_ventas hv 
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY TO_CHAR(hv.fecha_venta, 'YYYY-MM')
    ORDER BY anomes;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    # Mostrar en consola
    print(f"\n=== VENTAS POR MES - {anio} ===")
    if not resultados:
        print(f"❌ No se encontraron ventas para el año {anio}")
        
        # Consulta de diagnóstico
        debug_query = """
        SELECT TO_CHAR(hv.fecha_venta, 'YYYY') as año, COUNT(*) as total_ventas
        FROM analisis.hechos_ventas hv
        GROUP BY TO_CHAR(hv.fecha_venta, 'YYYY')
        ORDER BY año;
        """
        cursor.execute(debug_query)
        años_disponibles = cursor.fetchall()
        
        if años_disponibles:
            print("Años disponibles en la base de datos:")
            for año, total in años_disponibles:
                print(f"  - {año}: {total} ventas")
        else:
            print("❌ No hay datos de ventas en la tabla analisis.hechos_ventas")
        
        return []
    
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

        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(range(len(anomes))), y=cantidad, palette="Blues_d")

        plt.title(f'Ventas por mes - {anio}', fontsize=14, fontweight='bold')
        plt.xticks(range(len(anomes)), anomes, rotation=45)
        plt.ylabel('Cantidad de ventas')
        plt.xlabel('Mes')
        
        # Agregar valores en las barras
        for i, v in enumerate(cantidad):
            plt.text(i, v + max(cantidad) * 0.01, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        # Crear carpeta si no existe
        output_dir = "graficos"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/ventas_por_mes_{anio}.png"

        try:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✅ Gráfico guardado como: {filename}")
            print(f"📁 Ubicación: {os.path.abspath(filename)}")
        except Exception as e:
            print(f"❌ Error al guardar el gráfico: {e}")

        plt.show()
        plt.close()
    else:
        print("\n❌ No se encontraron resultados para ese año.")

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
        FROM analisis."Hechos_compras" hc
        WHERE TO_CHAR(hc.fecha_compra, 'YYYY') = %s
        GROUP BY compraAnomes
        ORDER BY compraAnomes
    ) AS comprames
    FULL JOIN
    (
        SELECT TO_CHAR(hv.fecha_venta, 'YYYY-MM') AS VentaAnomes,
               SUM(hv.monto) AS monto_ventas
        FROM analisis.hechos_ventas hv
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
    meses_raw = [fila[0] for fila in datos]
    ventas = [fila[1] for fila in datos]
    compras = [fila[2] for fila in datos]
    diferencias = [fila[3] for fila in datos]

    # Formatear los nombres de los meses
    meses = []
    for m in meses_raw:
        try:
            dt = datetime.strptime(m, "%Y-%m")
            meses.append(f"{calendar.month_name[dt.month]} {dt.year}")
        except:
            meses.append(m)

    # ---------- GRÁFICO DE BARRAS AGRUPADAS ----------
    x = np.arange(len(meses))
    ancho = 0.25

    plt.figure(figsize=(14, 6))
    plt.bar(x - ancho, ventas, width=ancho, label='Ventas', color='green')
    plt.bar(x, compras, width=ancho, label='Compras', color='blue')
    plt.bar(x + ancho, diferencias, width=ancho, label='Diferencia', color='red')

    plt.title(f'Comparación mensual de Compras, Ventas y Diferencia - {anio}')
    plt.xlabel('Mes')
    plt.ylabel('Monto (CLP)')
    plt.xticks(x, meses, rotation=45)
    plt.legend()
    plt.grid(axis='y')

    # Formatear el eje Y como CLP with separador de miles
    formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,} CLP".replace(",", "."))
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.tight_layout()

    # Crear carpeta si no existe
    output_dir = "graficos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/comparacion_barras_{anio}.png"
    plt.savefig(filename)
    plt.show()

    return datos
    
def top_10_modelos_mas_vendidos(conn, anio):
    query = """
    SELECT m.nombre_modelo,
           COUNT(*) AS cantidad_vendida
    FROM analisis.hechos_ventas hv
    JOIN analisis.modelos m ON hv.id_modelo = m.id_modelo
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY m.nombre_modelo
    ORDER BY cantidad_vendida DESC
    LIMIT 10;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    # Mostrar resultados en consola para debugging
    print(f"\n=== TOP 10 MODELOS MÁS VENDIDOS - {anio} ===")
    if not resultados:
        print(f"❌ No se encontraron ventas para el año {anio}")
        print("Verificando datos disponibles...")
        
        # Consulta de diagnóstico
        debug_query = """
        SELECT TO_CHAR(hv.fecha_venta, 'YYYY') as año, COUNT(*) as total_ventas
        FROM analisis.hechos_ventas hv
        GROUP BY TO_CHAR(hv.fecha_venta, 'YYYY')
        ORDER BY año;
        """
        cursor.execute(debug_query)
        años_disponibles = cursor.fetchall()
        
        if años_disponibles:
            print("Años disponibles en la base de datos:")
            for año, total in años_disponibles:
                print(f"  - {año}: {total} ventas")
        else:
            print("❌ No hay datos de ventas en la tabla analisis.hechos_ventas")
        
        return []
    
    # Mostrar resultados
    for i, (modelo, cantidad) in enumerate(resultados, 1):
        print(f"{i:2d}. {modelo}: {cantidad} unidades")

    # Extraer datos para el gráfico
    modelos = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    # Verificar que tenemos datos para graficar
    if not modelos or not cantidades:
        print("❌ No hay datos para generar el gráfico")
        return resultados

    # Truncar nombres largos de modelos para mejor visualización
    modelos_truncados = [textwrap.fill(modelo, 20) if len(modelo) > 20 else modelo for modelo in modelos]

    # Graficar
    plt.figure(figsize=(12, 8))
    barras = plt.barh(range(len(modelos_truncados)), cantidades, color='skyblue')
    
    # Configurar etiquetas y título
    plt.xlabel('Cantidad de unidades vendidas')
    plt.ylabel('Modelos')
    plt.title(f'Top 10 Modelos más Vendidos - {anio}', fontsize=14, fontweight='bold')
    
    # Configurar etiquetas del eje Y
    plt.yticks(range(len(modelos_truncados)), modelos_truncados)
    plt.gca().invert_yaxis()  # El más vendido arriba

    # Agregar valores en las barras
    for i, barra in enumerate(barras):
        ancho = barra.get_width()
        plt.text(ancho + max(cantidades) * 0.01, barra.get_y() + barra.get_height()/2,
                 str(int(ancho)), va='center', fontweight='bold')

    # Agregar grid para mejor lectura
    plt.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Crear carpeta si no existe
    output_dir = "graficos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/top_10_modelos_mas_vendidos_{anio}.png"
    
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico guardado como: {filename}")
        print(f"📁 Ubicación: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"❌ Error al guardar el gráfico: {e}")
    
    plt.show()
    plt.close()

    return resultados


def modelo_mas_vendido_por_region(conn, anio):
    query = """
    SELECT r.nombre_region, ranked.nombre_modelo, ranked.cantidad_vendida
    FROM (
        SELECT hv.id_region,
               m.nombre_modelo,
               COUNT(*) AS cantidad_vendida,
               ROW_NUMBER() OVER (PARTITION BY hv.id_region ORDER BY COUNT(*) DESC) AS fila
        FROM analisis.hechos_ventas hv
        JOIN analisis.modelos m ON hv.id_modelo = m.id_modelo
        WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
        GROUP BY hv.id_region, m.nombre_modelo
    ) ranked
    JOIN analisis.region r ON ranked.id_region = r.id_region
    WHERE ranked.fila = 1;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    if not resultados:
        print("\nNo se encontraron resultados para ese año en modelo más vendido por región.")
        return []

    # Ajustar nombres largos con saltos de línea y abreviaturas
    def abreviar_region(nombre):
        abreviaturas = {
            'Región de Arica y Parinacota': 'Arica y Parinacota',
            'Región de Tarapacá': 'Tarapacá',
            'Región de Antofagasta': 'Antofagasta',
            'Región de Atacama': 'Atacama',
            'Región de Coquimbo': 'Coquimbo',
            'Región de Valparaíso': 'Valparaíso',
            'Región Metropolitana de Santiago': 'RM',
            'Región del Libertador General Bernardo O’Higgins': 'O’Higgins',
            'Región del Maule': 'Maule',
            'Región de Ñuble': 'Ñuble',
            'Región del Biobío': 'Biobío',
            'Región de La Araucanía': 'Araucanía',
            'Región de Los Ríos': 'Los Ríos',
            'Región de Los Lagos': 'Los Lagos',
            'Región de Aysén del Gral. Carlos Ibáñez del Campo': 'Aysén',
            'Región de Magallanes y de la Antártica Chilena': 'Magallanes'
        }
        return abreviaturas.get(nombre, nombre)

    regiones = [abreviar_region(fila[0]) for fila in resultados]
    modelos = [fila[1] for fila in resultados]
    cantidades = [fila[2] for fila in resultados]
    etiquetas = [f"{modelo} ({cant} ventas)" for modelo, cant in zip(modelos, cantidades)]

    # Gráfico
    plt.figure(figsize=(max(12, len(regiones)*0.9), 6))
    barras = plt.bar(regiones, cantidades, color='mediumseagreen')
    plt.xticks(rotation=30, fontsize=9, ha='right')
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
                 fontsize=8, rotation=0)

    plt.tight_layout()
    # Crear carpeta si no existe
    output_dir = "graficos"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/modelo_mas_vendido_por_region_{anio}.png"
    plt.savefig(filename)
    plt.show()
    plt.close()
    
    print(f"\nGráfico guardado como: {filename}")
    print("Guardando gráfico en:", os.path.abspath(output_dir))

    return resultados




def comparacion_compras_vs_ventas_por_region(conn, anio):
    query = """
    SELECT r.nombre_region,
           COALESCE(vc.vendidos, 0) AS autos_vendidos,
           COALESCE(cc.comprados, 0) AS autos_comprados
    FROM (
        SELECT id_region, COUNT(*) AS vendidos
        FROM analisis.hechos_ventas
        WHERE TO_CHAR(fecha_venta, 'YYYY') = %s
        GROUP BY id_region
    ) vc
    FULL OUTER JOIN (
        SELECT id_region, COUNT(*) AS comprados
        FROM analisis."Hechos_compras"
        WHERE TO_CHAR(fecha_compra, 'YYYY') = %s
        GROUP BY id_region
    ) cc ON vc.id_region = cc.id_region
    JOIN analisis.region r ON r.id_region = COALESCE(vc.id_region, cc.id_region)
    ORDER BY r.id_region;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio, anio))
        resultados = cursor.fetchall()

    if resultados:
        # Abreviar nombres de regiones
        def abreviar_region(nombre):
            abreviaturas = {
                'Región de Arica y Parinacota': 'Arica y Parinacota',
                'Región de Tarapacá': 'Tarapacá',
                'Región de Antofagasta': 'Antofagasta',
                'Región de Atacama': 'Atacama',
                'Región de Coquimbo': 'Coquimbo',
                'Región de Valparaíso': 'Valparaíso',
                'Región Metropolitana de Santiago': 'RM',
                'Región del Libertador General Bernardo O’Higgins': 'O’Higgins',
                'Región del Maule': 'Maule',
                'Región de Ñuble': 'Ñuble',
                'Región del Biobío': 'Biobío',
                'Región de La Araucanía': 'Araucanía',
                'Región de Los Ríos': 'Los Ríos',
                'Región de Los Lagos': 'Los Lagos',
                'Región de Aysén del Gral. Carlos Ibáñez del Campo': 'Aysén',
                'Región de Magallanes y de la Antártica Chilena': 'Magallanes'
            }
            return abreviaturas.get(nombre, nombre)

        regiones = [abreviar_region(r[0]) for r in resultados]
        vendidos = [r[1] for r in resultados]
        comprados = [r[2] for r in resultados]

        x = range(len(regiones))
        width = 0.35

        plt.figure(figsize=(max(12, len(regiones)*0.9), 6))
        plt.bar([i - width/2 for i in x], vendidos, width=width, label='Vendidos', color='steelblue')
        plt.bar([i + width/2 for i in x], comprados, width=width, label='Comprados', color='darkorange')

        plt.xticks(x, regiones, rotation=30, fontsize=9, ha='right')
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
    FROM analisis.hechos_ventas hv
    JOIN analisis.autos a ON hv.id_auto = a.patente
    JOIN analisis.modelos m ON hv.id_modelo = m.id_modelo
    WHERE TO_CHAR(hv.fecha_venta, 'YYYY') = %s
    GROUP BY m.marca
    ORDER BY promedio_precio_venta DESC;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (anio,))
        resultados = cursor.fetchall()

    # Mostrar resultados en consola with format
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

def diagnosticar_datos(conn):
    """Función de diagnóstico para verificar qué datos están disponibles en la base de datos"""
    print("\n" + "="*60)
    print("               DIAGNÓSTICO DE DATOS")
    print("="*60)
    
    try:
        with conn.cursor() as cursor:
            # Verificar tabla hechos_ventas
            print("\n🔍 VERIFICANDO TABLA hechos_ventas:")
            cursor.execute("SELECT COUNT(*) FROM analisis.hechos_ventas;")
            total_ventas = cursor.fetchone()[0]
            print(f"   Total de registros: {total_ventas}")
            
            if total_ventas > 0:
                cursor.execute("""
                    SELECT TO_CHAR(fecha_venta, 'YYYY') as año, COUNT(*) as ventas
                    FROM analisis.hechos_ventas 
                    GROUP BY TO_CHAR(fecha_venta, 'YYYY')
                    ORDER BY año;
                """)
                años_ventas = cursor.fetchall()
                print("   Ventas por año:")
                for año, cantidad in años_ventas:
                    print(f"     - {año}: {cantidad} ventas")
                    
                cursor.execute("""
                    SELECT MIN(fecha_venta) as fecha_min, MAX(fecha_venta) as fecha_max
                    FROM analisis.hechos_ventas;
                """)
                fechas = cursor.fetchone()
                print(f"   Rango de fechas: {fechas[0]} a {fechas[1]}")
            
            # Verificar tabla modelos
            print("\n🔍 VERIFICANDO TABLA modelos:")
            cursor.execute("SELECT COUNT(*) FROM analisis.modelos;")
            total_modelos = cursor.fetchone()[0]
            print(f"   Total de modelos: {total_modelos}")
            
            if total_modelos > 0:
                cursor.execute("SELECT nombre_modelo FROM analisis.modelos LIMIT 5;")
                algunos_modelos = cursor.fetchall()
                print("   Algunos modelos:")
                for modelo in algunos_modelos:
                    print(f"     - {modelo[0]}")
            
            # Verificar relación ventas-modelos
            print("\n🔍 VERIFICANDO RELACIÓN ventas-modelos:")
            cursor.execute("""
                SELECT COUNT(DISTINCT hv.id_modelo) as modelos_vendidos,
                       COUNT(DISTINCT m.id_modelo) as modelos_totales
                FROM analisis.hechos_ventas hv
                FULL JOIN analisis.modelos m ON hv.id_modelo = m.id_modelo;
            """)
            relacion = cursor.fetchone()
            print(f"   Modelos que han tenido ventas: {relacion[0]}")
            print(f"   Total de modelos en catálogo: {relacion[1]}")
            
            # Verificar si hay problemas de JOIN
            cursor.execute("""
                SELECT COUNT(*) as ventas_sin_modelo
                FROM analisis.hechos_ventas hv
                LEFT JOIN analisis.modelos m ON hv.id_modelo = m.id_modelo
                WHERE m.id_modelo IS NULL;
            """)
            ventas_sin_modelo = cursor.fetchone()[0]
            if ventas_sin_modelo > 0:
                print(f"   ⚠️  ADVERTENCIA: {ventas_sin_modelo} ventas sin modelo asociado")
            
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
    
    print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description="Consulta base de datos por año")
    parser.add_argument("anio", help="Año para filtrar datos, formato YYYY")
    parser.add_argument("--diagnostico", "-d", action="store_true", 
                       help="Solo ejecutar diagnóstico de datos")
    args = parser.parse_args()
    
    try:
        conn = conectar()
        print(f"✅ Conexión a la base de datos exitosa")
        
        # Si solo se quiere diagnóstico
        if args.diagnostico:
            diagnosticar_datos(conn)
            conn.close()
            return
        
        print(f"\n{'='*50}")
        print(f"  REPORTE DE ANÁLISIS DE VENTAS - {args.anio}")
        print(f"{'='*50}")
        
        # Ejecutar diagnóstico primero
        diagnosticar_datos(conn)
        
        # Ejecutar consultas
        print(f"\n📊 VENTAS POR MES para el año {args.anio}:")
        ventas = ventas_por_mes(conn, args.anio)
        
        print(f"\n💰 COMPRAS, VENTAS Y DIFERENCIA para el año {args.anio}:")
        datos = compras_ventas_diferencia(conn, args.anio)
        for anomes, monto_ventas, monto_compras, diferencia in datos:
            print(f"{anomes}: Ventas=${monto_ventas:,.0f}, Compras=${monto_compras:,.0f}, Diferencia=${diferencia:,.0f}")
        
        print(f"\n🏆 TOP 10 MODELOS MÁS VENDIDOS en {args.anio}:")
        top_modelos = top_10_modelos_mas_vendidos(conn, args.anio)
        
        print(f"\n🗺️ MODELO MÁS VENDIDO POR REGIÓN en {args.anio}:")
        modelos_region = modelo_mas_vendido_por_region(conn, args.anio)
        for id_region, modelo, cantidad in modelos_region:
            print(f"Región {id_region}: {modelo} ({cantidad} ventas)")
        
        print(f"\n📈 COMPARACIÓN COMPRAS vs VENTAS POR REGIÓN en {args.anio}:")
        comparacion = comparacion_compras_vs_ventas_por_region(conn, args.anio)
        for id_region, vendidos, comprados in comparacion:
            print(f"Región {id_region}: Vendidos={vendidos}, Comprados={comprados}")
        
        print(f"\n💵 PROMEDIO DE PRECIO DE VENTA POR MARCA en {args.anio}:")
        precios = promedio_precio_venta_por_marca(conn, args.anio)
        
        print(f"\n{'='*50}")
        print("✅ Análisis completado exitosamente")
        print(f"📁 Los gráficos se han guardado en la carpeta 'graficos'")
        print(f"{'='*50}")

    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        try:
            conn.close()
        except:
            pass

    

if __name__ == "__main__":
    main()