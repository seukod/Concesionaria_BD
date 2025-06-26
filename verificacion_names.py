import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

# Crear conexión
conn = psycopg2.connect(**DB_CONFIG)

# Consulta de columnas y tablas
query = """
SELECT 
    table_name, 
    column_name, 
    data_type
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public'
ORDER BY 
    table_name, ordinal_position;
"""

# Leer resultado con pandas
df = pd.read_sql(query, conn)

# Cerrar conexión
conn.close()

print(df)
