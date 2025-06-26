"""
Módulo de utilidades de base de datos optimizado.
Implementa pool de conexiones y gestión eficiente de recursos.
"""

import psycopg2
from psycopg2 import pool
import threading
import atexit
from contextlib import contextmanager
from config import DB_CONFIG

class DatabaseManager:
    """
    Gestor de base de datos con pool de conexiones para mayor eficiencia.
    Implementa el patrón Singleton para una instancia única.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_pool = None
            self.initialized = True
            self._init_pool()
            # Registrar función de limpieza al salir
            atexit.register(self.close_all_connections)
    
    def _init_pool(self):
        """Inicializa el pool de conexiones"""
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,      # Mínimo 1 conexión
                maxconn=10,     # Máximo 10 conexiones
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            print("✅ Pool de conexiones inicializado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar pool de conexiones: {e}")
            self.connection_pool = None
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión del pool.
        Garantiza que la conexión se devuelva al pool automáticamente.
        """
        connection = None
        try:
            if self.connection_pool is None:
                # Fallback: crear conexión directa si el pool falla
                connection = psycopg2.connect(**DB_CONFIG)
                yield connection
            else:
                connection = self.connection_pool.getconn()
                if connection:
                    yield connection
                else:
                    raise Exception("No se pudo obtener conexión del pool")
        except Exception as e:
            if connection and not connection.closed:
                connection.rollback()
            raise e
        finally:
            if connection:
                if self.connection_pool is None:
                    # Conexión directa: cerrar manualmente
                    connection.close()
                else:
                    # Devolver conexión al pool
                    self.connection_pool.putconn(connection)
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Ejecuta una consulta usando el pool de conexiones.
        
        Args:
            query (str): Consulta SQL
            params (tuple): Parámetros para la consulta
            fetch (bool): Si True, devuelve resultados
        
        Returns:
            tuple: (columnas, filas) si fetch=True, None si fetch=False
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    
                    if fetch:
                        rows = cur.fetchall()
                        colnames = [desc[0] for desc in cur.description] if cur.description else []
                        return colnames, rows
                    else:
                        conn.commit()
                        return None
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            if fetch:
                return None, None
            return None
    
    def execute_many(self, query, params_list):
        """
        Ejecuta múltiples consultas en una sola transacción.
        Más eficiente para operaciones en lote.
        
        Args:
            query (str): Consulta SQL
            params_list (list): Lista de tuplas con parámetros
        
        Returns:
            bool: True si todas las operaciones fueron exitosas
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.executemany(query, params_list)
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error ejecutando consultas múltiples: {e}")
            return False
    
    def get_pool_status(self):
        """Obtiene información del estado del pool de conexiones"""
        if self.connection_pool is None:
            return "Pool no inicializado"
        
        try:
            # Información del pool (puede no estar disponible en todas las versiones)
            return {
                "conexiones_disponibles": "No disponible",
                "conexiones_en_uso": "No disponible",
                "pool_activo": True
            }
        except:
            return {"pool_activo": True}
    
    def close_all_connections(self):
        """Cierra todas las conexiones del pool"""
        if self.connection_pool:
            try:
                self.connection_pool.closeall()
                print("🔌 Pool de conexiones cerrado correctamente")
            except Exception as e:
                print(f"Error cerrando pool de conexiones: {e}")
    
    def test_connection(self):
        """Prueba la conectividad de la base de datos"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()
                    return result[0] == 1
        except Exception as e:
            print(f"Error probando conexión: {e}")
            return False

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

# Funciones de conveniencia para mantener compatibilidad
def get_connection():
    """Función de compatibilidad - usar db_manager.get_connection() directamente"""
    return db_manager.get_connection()

def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una consulta usando el pool de conexiones.
    
    Args:
        query (str): Consulta SQL
        params (tuple): Parámetros para la consulta
        fetch (bool): Si True, devuelve resultados
    
    Returns:
        tuple: (columnas, filas) si fetch=True, None si fetch=False
    """
    return db_manager.execute_query(query, params, fetch)

def execute_many(query, params_list):
    """
    Ejecuta múltiples consultas en una sola transacción.
    
    Args:
        query (str): Consulta SQL
        params_list (list): Lista de tuplas con parámetros
    
    Returns:
        bool: True si todas las operaciones fueron exitosas
    """
    return db_manager.execute_many(query, params_list)

def test_connection():
    """Prueba la conectividad de la base de datos"""
    return db_manager.test_connection()

def get_pool_status():
    """Obtiene información del estado del pool"""
    return db_manager.get_pool_status()

def close_all_connections():
    """Cierra todas las conexiones"""
    return db_manager.close_all_connections()

# Funciones específicas optimizadas
def create_row_optimized(table, columns, values):
    """Versión optimizada de create_row usando el pool"""
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO transaccional.{table} ({cols}) VALUES ({placeholders})"
    
    result = execute_query(query, values)
    return result is not None

def read_rows_optimized(table, columns=None, where_clause=None, where_values=None):
    """Versión optimizada de read_rows usando el pool"""
    select_cols = ', '.join(columns) if columns else '*'
    query = f"SELECT {select_cols} FROM transaccional.{table}"
    
    if where_clause:
        query += f" WHERE {where_clause}"
    
    return execute_query(query, where_values, fetch=True)

def update_row_optimized(table, key_column, key_value, columns, values):
    """Versión optimizada de update_row usando el pool"""
    set_clause = ', '.join([f"{col} = %s" for col in columns])
    query = f"UPDATE transaccional.{table} SET {set_clause} WHERE {key_column} = %s"
    
    result = execute_query(query, values + [key_value])
    return result is not None

def delete_row_optimized(table, key_column, key_value):
    """Versión optimizada de delete_row usando el pool"""
    query = f"DELETE FROM transaccional.{table} WHERE {key_column} = %s"
    
    result = execute_query(query, (key_value,))
    return result is not None

def batch_insert(table, columns, values_list):
    """
    Inserta múltiples filas en una sola transacción.
    Mucho más eficiente para grandes volúmenes de datos.
    
    Args:
        table (str): Nombre de la tabla
        columns (list): Lista de columnas
        values_list (list): Lista de listas con valores
    
    Returns:
        bool: True si la operación fue exitosa
    """
    if not values_list:
        return True
    
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO transaccional.{table} ({cols}) VALUES ({placeholders})"
    
    return execute_many(query, values_list)