"""
Módulo de utilidades CRUD genérico para operaciones de base de datos.
Proporciona funciones reutilizables para crear, leer, actualizar y eliminar registros.
"""

import psycopg2
import os
from config import DB_CONFIG

def limpiar_consola():
    """Limpia la consola del sistema"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_row(table, columns, values):
    """
    Inserta una fila en la tabla especificada.
    
    Args:
        table (str): Nombre de la tabla
        columns (list): Lista de nombres de columnas
        values (list): Lista de valores correspondientes
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cols = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO transaccional.{table} ({cols}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en create_row: {e}")
        return False

def read_rows(table, columns=None, where_clause=None, where_values=None):
    """
    Lee filas de la tabla especificada.
    
    Args:
        table (str): Nombre de la tabla
        columns (list, optional): Lista de columnas a seleccionar. Si es None, selecciona todas (*)
        where_clause (str, optional): Cláusula WHERE sin la palabra WHERE
        where_values (list, optional): Valores para la cláusula WHERE
    
    Returns:
        tuple: (nombres_columnas, filas)
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Construir la consulta
        select_cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {select_cols} FROM transaccional.{table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        # Ejecutar la consulta
        if where_values:
            cur.execute(query, where_values)
        else:
            cur.execute(query)
            
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return colnames, rows
    except Exception as e:
        print(f"Error en read_rows: {e}")
        return None, None

def update_row(table, key_column, key_value, columns, values):
    """
    Actualiza una fila en la tabla especificada.
    
    Args:
        table (str): Nombre de la tabla
        key_column (str): Nombre de la columna clave
        key_value: Valor de la clave
        columns (list): Lista de columnas a actualizar
        values (list): Lista de nuevos valores
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        set_clause = ', '.join([f"{col} = %s" for col in columns])
        query = f"UPDATE transaccional.{table} SET {set_clause} WHERE {key_column} = %s"
        cur.execute(query, values + [key_value])
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        return affected_rows > 0
    except Exception as e:
        print(f"Error en update_row: {e}")
        return False

def delete_row(table, key_column, key_value):
    """
    Elimina una fila de la tabla especificada.
    
    Args:
        table (str): Nombre de la tabla
        key_column (str): Nombre de la columna clave
        key_value: Valor de la clave
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = f"DELETE FROM transaccional.{table} WHERE {key_column} = %s"
        cur.execute(query, (key_value,))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        return affected_rows > 0
    except Exception as e:
        print(f"Error en delete_row: {e}")
        return False

def execute_custom_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL personalizada.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (list, optional): Parámetros para la consulta
        fetch (bool): Si True, retorna los resultados. Si False, solo ejecuta la consulta.
    
    Returns:
        tuple: (nombres_columnas, filas) si fetch=True, sino None
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        if fetch:
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description] if cur.description else []
            result = (colnames, rows)
        else:
            conn.commit()
            result = None
            
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error en execute_custom_query: {e}")
        return None if fetch else False

def table_exists(table_name):
    """
    Verifica si una tabla existe en el esquema transaccional.
    
    Args:
        table_name (str): Nombre de la tabla
    
    Returns:
        bool: True si la tabla existe, False en caso contrario
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'transaccional' 
                AND table_name = %s
            );
        """, (table_name,))
        exists = cur.fetchone()[0]
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error verificando existencia de tabla: {e}")
        return False

def get_table_columns(table_name):
    """
    Obtiene los nombres de las columnas de una tabla.
    
    Args:
        table_name (str): Nombre de la tabla
    
    Returns:
        list: Lista de nombres de columnas
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'transaccional' 
            AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return columns
    except Exception as e:
        print(f"Error obteniendo columnas de tabla: {e}")
        return []
