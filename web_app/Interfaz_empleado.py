from db import get_connection, ejecutar_consulta
import streamlit as st
import pandas as pd
from datetime import datetime

from web_app.models.empleados import obtener_empleados

# Almacenamiento en memoria
if "reporte_empleados" not in st.session_state:
    st.session_state.reporte_empleados = []


def report_activity(id, employee_name, email, rol, active):
    st.session_state.reporte_empleados.append({
        "Id": id,
        "Nombre": employee_name,
        "Correo": email,
        "Rol": rol,
        "Activo": active,
        "Acciones": [
            {"label": "Editar", "action": "edit"},
            {"label": "Eliminar", "action": "delete"}
        ]
    })


st.title("Employee Activity Reporting")


def empleados():
    lista = obtener_empleados()  # Obtiene la lista de empleados
    if not lista:
        st.error("No employees found.")
        return []

    return lista


lista = empleados()  # Obtiene la lista de empleados
if not lista:
    st.error("No employees found.")
    st.stop()
else:
    for empleado in lista:
        report_activity(
            empleado['id_empleado'],
            empleado['nombre'],
            empleado['correo'],
            empleado['rol'],
            empleado['activo']
        )


# """ # Sección de reporte
# st.header("Report an Activity")
# employee_name = st.text_input("Employee Name")
# activity = st.selectbox("Select Activity", activities)
# comments = st.text_area("Comments")
# quality = st.slider("Quality (1-5)", 1, 5)
# if st.button("Report Activity"):
#     report_activity(employee_name, activity, comments, quality)
#     st.success("Activity reported successfully!")
#  """
# Sección de resumen
# st.header("Monthly Activity Summary")
if st.session_state.reporte_empleados:
    df = pd.DataFrame(st.session_state.reporte_empleados)
    st.dataframe(df)
else:
    st.write("No activities reported yet.")
