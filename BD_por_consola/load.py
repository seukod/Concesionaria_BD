from .db_utils import execute_query

def load_data(data):
    for row in data:
        query = "INSERT INTO tabla (col1, col2) VALUES (%s, %s)"
        params = (row["col1"], row["col2"])
        execute_query(query, params)