import streamlit as st
import pandas as pd
from db import get_connection, ejecutar_consulta

st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

# Función para cargar tablas


def cargar_tabla(nombre_tabla):
    try:
        resultado = ejecutar_consulta(
            conexion, f"SELECT * FROM {nombre_tabla}")
        if isinstance(resultado, list):
            return pd.DataFrame(resultado)
        elif isinstance(resultado, pd.DataFrame):
            return resultado
        else:
            st.warning(
                f"No se pudo interpretar el resultado de {nombre_tabla}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar {nombre_tabla}: {e}")
        return pd.DataFrame()


# Función para mostrar resumen mensual


def mostrar_resumen_mensual():
    st.subheader("Resumen Mensual de Actividades por Empleado")
    resumen = reportes.groupby("id_empleado").agg(
        total_actividades=pd.NamedAgg(column="id_actividad", aggfunc="count"),
        actividades_reportadas=pd.NamedAgg(
            column="acciones_realizadas", aggfunc="count")
    ).reset_index()
    resumen = resumen.merge(empleados, on="id_empleado", how="left")
    st.dataframe(resumen)

# Función para mostrar menú de administración de tablas


def mostrar_menu_administracion():
    st.subheader("Administración de Tablas")
    tablas = ["Empleados", "Contratos",
              "Actividades", "Reportes", "Notificaciones"]
    tabla_seleccionada = st.selectbox(
        "Selecciona una tabla para administrar", tablas, key="tabla_admin")
    print(f"Tabla seleccionada: {tabla_seleccionada}")

    if tabla_seleccionada:
        datos = cargar_tabla(tabla_seleccionada)

        st.markdown(f"### {tabla_seleccionada}")
        st.button(f"Nuevo {tabla_seleccionada[:-1]}", key="nuevo_btn")

        if not datos.empty:
            datos['Acciones'] = datos.apply(lambda row: f"""
                <button style='background-color: yellow;'>Editar</button>
                <button style='background-color: red;'>Eliminar</button>
            """, axis=1)
            st.write(datos.to_html(escape=False, index=False),
                     unsafe_allow_html=True)
        else:
            st.info("No hay datos disponibles para esta tabla.")

# Función para enviar notificaciones


def enviar_notificaciones():
    st.subheader("Enviar Notificaciones")
    empleados_lista = empleados["nombre"].tolist()
    empleado_seleccionado = st.selectbox(
        "Selecciona un empleado", empleados_lista)
    mensaje = st.text_area("Mensaje")
    if st.button("Enviar"):
        id_empleado = empleados[empleados["nombre"] ==
                                empleado_seleccionado]["id_empleado"].values[0]
        consulta = f"""
            INSERT INTO Notificaciones (id_empleado, mensaje, fecha_envio, leido)
            VALUES ({id_empleado}, '{mensaje}', GETDATE(), 0)
        """
        ejecutar_consulta(conexion, consulta)
        st.success("Notificación enviada")

# Función para mostrar resumen personal del empleado


def mostrar_resumen_personal(id_empleado):
    st.subheader("Resumen Personal")
    resumen = reportes[reportes["id_empleado"] == id_empleado].groupby("id_actividad").agg(
        total_actividades=pd.NamedAgg(column="id_actividad", aggfunc="count"),
        actividades_reportadas=pd.NamedAgg(
            column="acciones_realizadas", aggfunc="count")
    ).reset_index()
    resumen = resumen.merge(actividades, on="id_actividad", how="left")
    st.dataframe(resumen)

# Función para agregar acción


def agregar_accion(id_empleado):
    st.subheader("Agregar Acción")
    actividades_lista = actividades["descripcion"].tolist()
    actividad_seleccionada = st.selectbox(
        "Selecciona una actividad", actividades_lista)
    acciones_realizadas = st.text_area("Acciones Realizadas")
    comentarios = st.text_area("Comentarios")
    porcentaje = st.slider("Calificación de Calidad", 0, 100, 50)
    if st.button("Agregar"):
        id_actividad = actividades[actividades["descripcion"]
                                   == actividad_seleccionada]["id_actividad"].values[0]
        consulta = f"""
            INSERT INTO Reportes (id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado)
            VALUES ({id_empleado}, {id_actividad}, GETDATE(), '{acciones_realizadas}', '{comentarios}', {porcentaje}, '', 0)
        """
        ejecutar_consulta(conexion, consulta)
        st.success("Acción agregada")


# Inicio de sesión
st.sidebar.header("Inicio de Sesión")
usuario = st.sidebar.text_input("Usuario")
contrasena = st.sidebar.text_input("Contraseña", type="password")
rol = st.sidebar.selectbox("Rol", ["Administrador", "Empleado"])

if st.sidebar.button("Iniciar Sesión"):
    conexion = get_connection()
    empleados = cargar_tabla("Empleados")
    contratos = cargar_tabla("Contratos")
    actividades = cargar_tabla("Actividades")
    reportes = cargar_tabla("Reportes")
    notificaciones = cargar_tabla("Notificaciones")

    if rol == "Administrador":
        st.sidebar.success("Sesión iniciada como Administrador")
        mostrar_resumen_mensual()
        mostrar_menu_administracion()
        enviar_notificaciones()

    elif rol == "Empleado":
        st.sidebar.success("Sesión iniciada como Empleado")
        if usuario in empleados["nombre"].values:
            id_empleado = empleados[empleados["nombre"]
                                    == usuario]["id_empleado"].values[0]
            mostrar_resumen_personal(id_empleado)
            agregar_accion(id_empleado)
        else:
            st.error("Empleado no encontrado.")
