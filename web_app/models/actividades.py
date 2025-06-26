from db import get_connection, ejecutar_consulta
from logger import logger


def obtener_actividades():
    try:
        conn = get_connection()
        consulta = "SELECT id_actividad, Nro, descripcion, id_contrato, porcentaje FROM Actividades"
        rows = ejecutar_consulta(conn, consulta)
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error obteniendo actividades: {e}")
        return []


def obtener_actividad(id_actividad):
    try:
        conn = get_connection()
        consulta = f"SELECT * FROM Actividades WHERE id_actividad={id_actividad}"
        row = ejecutar_consulta(conn, consulta)
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error obteniendo actividad: {e}")
        return None


def crear_actividad(nro, descripcion, id_contrato, porcentaje):
    try:
        conn = get_connection()
        consulta = "INSERT INTO Actividades (Nro, descripcion, id_contrato, porcentaje) VALUES (?, ?, ?, ?)"
        ejecutar_consulta(
            conn, consulta, (nro, descripcion, id_contrato, porcentaje))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error creando actividad: {e}")
        return False


def actualizar_actividad(id_actividad, nro, descripcion, id_contrato, porcentaje):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Actividades SET Nro=?, descripcion=?, id_contrato=?, porcentaje=? WHERE id_actividad=?",
            (nro, descripcion, id_contrato, porcentaje, id_actividad)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error actualizando actividad: {e}")
        return False


def eliminar_actividad(id_actividad):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Actividades WHERE id_actividad=?", id_actividad)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error eliminando actividad: {e}")
        return False
