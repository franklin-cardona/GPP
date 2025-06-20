
import pyodbc
from logger import logger

def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=db_gpc;'
            'Trusted_Connection=yes;'
        )
        logger.info("Conexión exitosa a la base de datos.")
        return conn
    except Exception as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        raise
