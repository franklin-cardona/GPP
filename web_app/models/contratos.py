from db import get_connection
from logger import logger

def obtener_contratos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Se une con Empleados para mostrar el nombre del empleado
        cursor.execute("SELECT c.id_contrato, c.nombre_contrato, c.fecha_inicio, c.fecha_fin, c.id_empleado, e.nombre AS nombre_empleado FROM Contratos c LEFT JOIN Empleados e ON c.id_empleado = e.id_empleado")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error obteniendo contratos: {e}")
        return []

def obtener_contrato(id_contrato):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_contrato, nombre_contrato, fecha_inicio, fecha_fin, id_empleado FROM Contratos WHERE id_contrato=?", id_contrato)
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        logger.error(f"Error obteniendo contrato: {e}")
        return None

def crear_contrato(nombre_contrato, fecha_inicio, fecha_fin, id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Contratos (nombre_contrato, fecha_inicio, fecha_fin, id_empleado) VALUES (?, ?, ?, ?)",
            (nombre_contrato, fecha_inicio, fecha_fin, id_empleado if id_empleado else None) # Permite NULL
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error creando contrato: {e}")
        return False

def actualizar_contrato(id_contrato, nombre_contrato, fecha_inicio, fecha_fin, id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Contratos SET nombre_contrato=?, fecha_inicio=?, fecha_fin=?, id_empleado=? WHERE id_contrato=?",
            (nombre_contrato, fecha_inicio, fecha_fin, id_empleado if id_empleado else None, id_contrato)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error actualizando contrato: {e}")
        return False

def eliminar_contrato(id_contrato):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Contratos WHERE id_contrato=?", id_contrato)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error eliminando contrato: {e}")
        return False