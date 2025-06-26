
import pyodbc
import duckdb
import pandas as pd
from logger import logger


def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=db_gpc;'
            'Trusted_Connection=yes;'
        )
        print("Conexión exitosa a la base de datos SQL Server.")
        logger.info("Conexión exitosa a la base de datos SQL Server.")
        return conn
    except Exception as e:
        print(f"Error de conexión a SQL Server: {e}")
        logger.error(f"Error de conexión a SQL Server: {e}")
        print("Intentando conectarse al archivo Excel...")

        try:
            # Cargar todas las hojas del archivo Excel
            excel_file = 'Basedatos.xlsx'
            sheets = pd.read_excel(excel_file, sheet_name=None)

            # Crear conexión DuckDB en memoria
            con = duckdb.connect()
            print("Conexión a DuckDB creada en memoria.")
            logger.info("Conexión a DuckDB creada en memoria.")
            # Registrar cada hoja como tabla
            for sheet_name, df in sheets.items():
                con.register(sheet_name, df)
                print(
                    f"Hoja '{sheet_name}' registrada como tabla en DuckDB. {len(df)} filas.")
                logger.info(
                    f"Hoja '{sheet_name}' registrada como tabla en DuckDB.")

            print("Conexión exitosa al archivo Excel con DuckDB.")
            logger.info("Conexión exitosa al archivo Excel con DuckDB.")
            return con
        except Exception as ex:
            print(f"Error al conectarse al archivo Excel: {ex}")
            logger.error(f"Error al conectarse al archivo Excel: {ex}")
            return None


def ejecutar_consulta(conexion, consulta):
    if isinstance(conexion, pyodbc.Connection):
        # Conexión a SQL Server
        cursor = conexion.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        return [dict(zip(columnas, fila)) for fila in resultados]

    elif isinstance(conexion, duckdb.DuckDBPyConnection):
        # Conexión a Excel vía DuckDB
        df = conexion.execute(consulta).fetchdf()
        print(df.to_dict(orient='records'))
        return df.to_dict(orient='records')

    else:
        raise ValueError("Tipo de conexión no soportado.")
