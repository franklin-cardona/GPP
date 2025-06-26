from db import get_connection, ejecutar_consulta
from logger import logger


def obtener_empleados():
    try:
        conn = get_connection()
        consulta = "SELECT id_empleado, nombre, correo, rol, activo FROM Empleados"
        rows = ejecutar_consulta(conn, consulta)
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error obteniendo empleados: {e}")
        return []


def obtener_empleado(id_empleado):
    try:
        conn = get_connection()
        consulta = f"SELECT id_empleado, nombre, correo, rol, activo FROM Empleados WHERE id_empleado={id_empleado}"
        row = ejecutar_consulta(conn, consulta)
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error obteniendo empleado: {e}")
        return None


def crear_empleado(nombre, correo, rol, activo):
    try:
        conn = get_connection()
        consulta = "INSERT INTO Empleados (nombre, correo, rol, activo) VALUES (?, ?, ?, ?)"
        ejecutar_consulta(
            conn, consulta, (nombre, correo, rol, activo)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error creando empleado: {e}")
        return False


def actualizar_empleado(id_empleado, nombre, correo, rol, activo):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Empleados SET nombre=?, correo=?, rol=?, activo=? WHERE id_empleado=?",
            (nombre, correo, rol, activo, id_empleado)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error actualizando empleado: {e}")
        return False


def eliminar_empleado(id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Empleados WHERE id_empleado=?", id_empleado)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error eliminando empleado: {e}")
        return False
