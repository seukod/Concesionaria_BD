import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

def get_connection():
    return psycopg2.connect(
        host="aws-0-sa-east-1.pooler.supabase.com",
        password="0NzSHHo6Ee9Hl4BI",
        port="5432",
        database="postgres",
        user="postgres.qdxsvygmfuqrrcaisqvw"
    )

def ventas_por_mes(anio):
    conn = get_connection()
    query = f"""
        SELECT 
            EXTRACT(MONTH FROM fecha_venta) AS mes, 
            COUNT(*) AS cantidad
        FROM ventas
        WHERE EXTRACT(YEAR FROM fecha_venta) = {anio}
        GROUP BY mes
        ORDER BY mes;
    """
    # Opción alternativa con read_sql_query y cursor
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print(f"No hay datos de ventas para el año {anio}")
        return

    plt.figure(figsize=(10,5))
    sns.barplot(x='mes', y='cantidad', data=df, palette='Blues_d')
    plt.title(f"Ventas por mes en {anio}")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de ventas")
    plt.show()
ventas_por_mes(2025)
ventas_por_mes(2024)
ventas_por_mes(2023)
ventas_por_mes(2022)


