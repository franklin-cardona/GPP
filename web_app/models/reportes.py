from db import get_connection, ejecutar_consulta
from logger import logger


def obtener_reportes():
    try:
        conn = get_connection()
        consulta = """
            SELECT
                r.id_reporte,
                r.id_empleado,
                e.nombre AS nombre_empleado,
                r.id_actividad,
                a.descripcion AS descripcion_actividad,
                r.fecha,
                r.acciones_realizadas,
                r.comentarios,
                r.porcentaje,
                r.entregable,
                r.estado
            FROM Reportes r
            JOIN Empleados e ON r.id_empleado = e.id_empleado
            JOIN Actividades a ON r.id_actividad = a.id_actividad
        """
        rows = ejecutar_consulta(conn, consulta)
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error obteniendo reportes: {e}")
        return []


def obtener_reporte(id_reporte):
    try:
        conn = get_connection()
        consulta = f"SELECT id_reporte, id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado FROM Reportes WHERE id_reporte={id_reporte}"
        row = ejecutar_consulta(conn, consulta)
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error obteniendo reporte: {e}")
        return None


def crear_reporte(id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado):
    try:
        conn = get_connection()
        consulta = "INSERT INTO Reportes (id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        ejecutar_consulta(
            conn, consulta, (id_empleado, id_actividad, fecha,
                             acciones_realizadas, comentarios, porcentaje, entregable, estado)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error creando reporte: {e}")
        return False


def actualizar_reporte(id_reporte, id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Reportes SET id_empleado=?, id_actividad=?, fecha=?, acciones_realizadas=?, comentarios=?, porcentaje=?, entregable=?, estado=? WHERE id_reporte=?",
            (id_empleado, id_actividad, fecha, acciones_realizadas,
             comentarios, porcentaje, entregable, estado, id_reporte)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error actualizando reporte: {e}")
        return False


def eliminar_reporte(id_reporte):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Reportes WHERE id_reporte=?", id_reporte)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error eliminando reporte: {e}")
        return False
