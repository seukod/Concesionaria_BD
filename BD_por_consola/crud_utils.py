"""
Módulo de utilidades CRUD genérico optimizado.
Utiliza pool de conexiones para mayor eficiencia.
"""

import os
from config import DB_CONFIG
from db_utils import (
    execute_query, 
    db_manager,
    create_row_optimized,
    read_rows_optimized, 
    update_row_optimized,
    delete_row_optimized,
    batch_insert
)

def limpiar_consola():
    """Limpia la consola del sistema"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_row(table, columns, values):
    """
    Inserta una fila en la tabla especificada usando pool de conexiones.
    
    Args:
        table (str): Nombre de la tabla
        columns (list): Lista de nombres de columnas
        values (list): Lista de valores correspondientes
    
    Returns:
        bool: True si la operación fue exitosa
    """
    try:
        return create_row_optimized(table, columns, values)
    except Exception as e:
        print(f"Error en create_row: {e}")
        return False

def read_rows(table, columns=None, where_clause=None, where_values=None):
    """
    Lee filas de la tabla especificada usando pool de conexiones.
    
    Args:
        table (str): Nombre de la tabla
        columns (list, optional): Lista de columnas a seleccionar. Si es None, selecciona todas (*)
        where_clause (str, optional): Cláusula WHERE sin la palabra WHERE
        where_values (list, optional): Valores para la cláusula WHERE
    
    Returns:
        tuple: (nombres_columnas, filas)
    """
    try:
        return read_rows_optimized(table, columns, where_clause, where_values)
    except Exception as e:
        print(f"Error en read_rows: {e}")
        return None, None

def update_row(table, key_column, key_value, columns, values):
    """
    Actualiza una fila en la tabla especificada usando pool de conexiones.
    
    Args:
        table (str): Nombre de la tabla
        key_column (str): Nombre de la columna clave
        key_value: Valor de la clave
        columns (list): Lista de columnas a actualizar
        values (list): Lista de nuevos valores
    
    Returns:
        bool: True si la operación fue exitosa
    """
    try:
        return update_row_optimized(table, key_column, key_value, columns, values)
    except Exception as e:
        print(f"Error en update_row: {e}")
        return False

def delete_row(table, key_column, key_value):
    """
    Elimina una fila de la tabla especificada usando pool de conexiones.
    
    Args:
        table (str): Nombre de la tabla
        key_column (str): Nombre de la columna clave
        key_value: Valor de la clave
    
    Returns:
        bool: True si la operación fue exitosa
    """
    try:
        return delete_row_optimized(table, key_column, key_value)
    except Exception as e:
        print(f"Error en delete_row: {e}")
        return False

def execute_custom_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL personalizada usando pool de conexiones.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (list, optional): Parámetros para la consulta
        fetch (bool): Si True, retorna los resultados. Si False, solo ejecuta la consulta.
    
    Returns:
        tuple: (nombres_columnas, filas) si fetch=True, sino None
    """
    try:
        if fetch:
            return execute_query(query, params, fetch=True)
        else:
            result = execute_query(query, params, fetch=False)
            return result is not None
    except Exception as e:
        print(f"Error en execute_custom_query: {e}")
        return None if fetch else False

def table_exists(table_name):
    """
    Verifica si una tabla existe en el esquema transaccional usando pool de conexiones.
    
    Args:
        table_name (str): Nombre de la tabla
    
    Returns:
        bool: True si la tabla existe, False en caso contrario
    """
    try:
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'transaccional' 
                AND table_name = %s
            );
        """
        colnames, result = execute_query(query, (table_name,), fetch=True)
        return result[0][0] if result else False
    except Exception as e:
        print(f"Error verificando existencia de tabla: {e}")
        return False

def get_table_columns(table_name):
    """
    Obtiene los nombres de las columnas de una tabla usando pool de conexiones.
    
    Args:
        table_name (str): Nombre de la tabla
    
    Returns:
        list: Lista de nombres de columnas
    """
    try:
        query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'transaccional' 
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        colnames, result = execute_query(query, (table_name,), fetch=True)
        return [row[0] for row in result] if result else []
    except Exception as e:
        print(f"Error obteniendo columnas de tabla: {e}")
        return []

def bulk_insert(table, columns, values_list):
    """
    Inserta múltiples filas de manera eficiente usando una sola transacción.
    
    Args:
        table (str): Nombre de la tabla
        columns (list): Lista de nombres de columnas
        values_list (list): Lista de listas con valores para cada fila
    
    Returns:
        bool: True si todas las inserciones fueron exitosas
    """
    try:
        return batch_insert(table, columns, values_list)
    except Exception as e:
        print(f"Error en bulk_insert: {e}")
        return False

def get_table_info(table_name):
    """
    Obtiene información detallada de una tabla.
    
    Args:
        table_name (str): Nombre de la tabla
    
    Returns:
        dict: Información de la tabla (columnas, tipos, etc.)
    """
    try:
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_schema = 'transaccional' 
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        colnames, result = execute_query(query, (table_name,), fetch=True)
        
        if result:
            columns_info = []
            for row in result:
                columns_info.append({
                    'name': row[0],
                    'type': row[1],
                    'nullable': row[2] == 'YES',
                    'default': row[3]
                })
            return {
                'table_name': table_name,
                'columns': columns_info,
                'column_count': len(columns_info)
            }
        return None
    except Exception as e:
        print(f"Error obteniendo información de tabla: {e}")
        return None

def execute_transaction(operations):
    """
    Ejecuta múltiples operaciones en una sola transacción.
    
    Args:
        operations (list): Lista de tuplas (query, params)
    
    Returns:
        bool: True si todas las operaciones fueron exitosas
    """
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                for query, params in operations:
                    cur.execute(query, params)
                conn.commit()
                return True
    except Exception as e:
        print(f"Error ejecutando transacción: {e}")
        return False

def get_record_count(table, where_clause=None, where_values=None):
    """
    Obtiene el número de registros en una tabla.
    
    Args:
        table (str): Nombre de la tabla
        where_clause (str, optional): Cláusula WHERE
        where_values (list, optional): Valores para WHERE
    
    Returns:
        int: Número de registros
    """
    try:
        query = f"SELECT COUNT(*) FROM transaccional.{table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        colnames, result = execute_query(query, where_values, fetch=True)
        return result[0][0] if result else 0
    except Exception as e:
        print(f"Error obteniendo conteo de registros: {e}")
        return 0

def check_database_health():
    """
    Verifica el estado de salud de la base de datos y las conexiones.
    
    Returns:
        dict: Estado de salud del sistema
    """
    try:
        # Probar conexión básica
        test_query = "SELECT 1"
        colnames, result = execute_query(test_query, fetch=True)
        connection_ok = result is not None
        
        # Verificar pool de conexiones
        pool_status = db_manager.get_pool_status()
        
        # Verificar esquema transaccional
        schema_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'transaccional'"
        colnames, schema_result = execute_query(schema_query, fetch=True)
        schema_exists = len(schema_result) > 0 if schema_result else False
        
        return {
            'connection_ok': connection_ok,
            'pool_status': pool_status,
            'schema_exists': schema_exists,
            'timestamp': 'now()'
        }
    except Exception as e:
        return {
            'connection_ok': False,
            'error': str(e),
            'timestamp': 'now()'
        }
