
from flask import Flask, render_template, request, redirect, url_for, flash
from models.actividades import (
    obtener_actividades,
    obtener_actividad,
    crear_actividad,
    actualizar_actividad,
    eliminar_actividad
)
from models.empleados import (
    obtener_empleados,
    obtener_empleado,
    crear_empleado,
    actualizar_empleado,
    eliminar_empleado
)
from models.contratos import (
    obtener_contratos,
    obtener_contrato,
    crear_contrato,
    actualizar_contrato,
    eliminar_contrato
)
from models.reportes import (
    obtener_reportes,
    obtener_reporte,
    crear_reporte,
    actualizar_reporte,
    eliminar_reporte
)
from logger import logger
from datetime import datetime # Importar datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def index():
    return '<h1>Página de inicio de Gestión de Proyectos y Contratos</h1><p>Navega a /actividades, /empleados, /contratos o /reportes para ver los listados.</p>'

# --- Rutas para Actividades (Ya existentes) ---
@app.route('/actividades')
def actividades():
    lista = obtener_actividades()
    return render_template('actividades/index.html', actividades=lista)

@app.route('/actividades/nueva', methods=['GET', 'POST'])
def nueva_actividad():
    if request.method == 'POST':
        nro = request.form['nro']
        descripcion = request.form['descripcion']
        id_contrato = request.form['id_contrato']
        porcentaje = request.form['porcentaje']
        if crear_actividad(nro, descripcion, id_contrato, porcentaje):
            flash("Actividad creada con éxito.", "success")
        else:
            flash("Error al crear la actividad.", "danger")
        return redirect(url_for('actividades'))
    # Necesitamos pasar los contratos para el select en el formulario
    contratos = obtener_contratos()
    return render_template('actividades/form.html', actividad=None, contratos=contratos)


@app.route('/actividades/editar/<int:id>', methods=['GET', 'POST'])
def editar_actividad(id):
    actividad = obtener_actividad(id)
    if not actividad:
        flash("Actividad no encontrada.", "danger")
        return redirect(url_for('actividades'))

    if request.method == 'POST':
        nro = request.form['nro']
        descripcion = request.form['descripcion']
        id_contrato = request.form['id_contrato']
        porcentaje = request.form['porcentaje']
        if actualizar_actividad(id, nro, descripcion, id_contrato, porcentaje):
            flash("Actividad actualizada con éxito.", "success")
        else:
            flash("Error al actualizar la actividad.", "danger")
        return redirect(url_for('actividades'))
    contratos = obtener_contratos()
    return render_template('actividades/form.html', actividad=actividad, contratos=contratos)

@app.route('/actividades/eliminar/<int:id>')
def eliminar_actividad_route(id):
    if eliminar_actividad(id):
        flash("Actividad eliminada con éxito.", "success")
    else:
        flash("Error al eliminar la actividad.", "danger")
    return redirect(url_for('actividades'))

# --- Rutas para Empleados ---
@app.route('/empleados')
def empleados():
    lista = obtener_empleados()
    return render_template('empleados/index.html', empleados=lista)

@app.route('/empleados/nuevo', methods=['GET', 'POST'])
def nuevo_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']
        activo = 'activo' in request.form # Checkbox
        if crear_empleado(nombre, correo, rol, activo):
            flash("Empleado creado con éxito.", "success")
        else:
            flash("Error al crear el empleado. El correo ya podría existir.", "danger")
        return redirect(url_for('empleados'))
    return render_template('empleados/form.html', empleado=None)

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    empleado = obtener_empleado(id)
    if not empleado:
        flash("Empleado no encontrado.", "danger")
        return redirect(url_for('empleados'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']
        activo = 'activo' in request.form
        if actualizar_empleado(id, nombre, correo, rol, activo):
            flash("Empleado actualizado con éxito.", "success")
        else:
            flash("Error al actualizar el empleado. El correo ya podría existir para otro empleado.", "danger")
        return redirect(url_for('empleados'))
    return render_template('empleados/form.html', empleado=empleado)

@app.route('/empleados/eliminar/<int:id>')
def eliminar_empleado_route(id):
    if eliminar_empleado(id):
        flash("Empleado eliminado con éxito.", "success")
    else:
        flash("Error al eliminar el empleado. Podría tener contratos asociados.", "danger")
    return redirect(url_for('empleados'))

# --- Rutas para Contratos ---
@app.route('/contratos')
def contratos():
    lista = obtener_contratos()
    return render_template('contratos/index.html', contratos=lista)

@app.route('/contratos/nuevo', methods=['GET', 'POST'])
def nuevo_contrato():
    if request.method == 'POST':
        nombre_contrato = request.form['nombre_contrato']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        id_empleado = request.form['id_empleado']
        if crear_contrato(nombre_contrato, fecha_inicio, fecha_fin, id_empleado):
            flash("Contrato creado con éxito.", "success")
        else:
            flash("Error al crear el contrato.", "danger")
        return redirect(url_for('contratos'))
    empleados = obtener_empleados()
    return render_template('contratos/form.html', contrato=None, empleados=empleados)

@app.route('/contratos/editar/<int:id>', methods=['GET', 'POST'])
def editar_contrato(id):
    contrato = obtener_contrato(id)
    if not contrato:
        flash("Contrato no encontrado.", "danger")
        return redirect(url_for('contratos'))

    if request.method == 'POST':
        nombre_contrato = request.form['nombre_contrato']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        id_empleado = request.form['id_empleado']
        if actualizar_contrato(id, nombre_contrato, fecha_inicio, fecha_fin, id_empleado):
            flash("Contrato actualizado con éxito.", "success")
        else:
            flash("Error al actualizar el contrato.", "danger")
        return redirect(url_for('contratos'))
    empleados = obtener_empleados()
    return render_template('contratos/form.html', contrato=contrato, empleados=empleados)

@app.route('/contratos/eliminar/<int:id>')
def eliminar_contrato_route(id):
    if eliminar_contrato(id):
        flash("Contrato eliminado con éxito.", "success")
    else:
        flash("Error al eliminar el contrato. Podría tener actividades asociadas.", "danger")
    return redirect(url_for('contratos'))

# --- Rutas para Reportes ---
@app.route('/reportes')
def reportes():
    lista = obtener_reportes()
    return render_template('reportes/index.html', reportes=lista)

@app.route('/reportes/nuevo', methods=['GET', 'POST'])
def nuevo_reporte():
    if request.method == 'POST':
        id_empleado = request.form['id_empleado']
        id_actividad = request.form['id_actividad']
        
        # Convertir la cadena de fecha a objeto datetime
        fecha_str = request.form['fecha']
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
        except ValueError as e:
            flash(f"Formato de fecha u hora inválido: {e}", "danger")
            empleados = obtener_empleados()
            actividades = obtener_actividades()
            return render_template('reportes/form.html', reporte=None, empleados=empleados, actividades=actividades)

        acciones_realizadas = request.form['acciones_realizadas']
        comentarios = request.form['comentarios']
        porcentaje = request.form['porcentaje']
        entregable = request.form['entregable']
        estado = 'estado' in request.form
        
        if crear_reporte(id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado):
            flash("Reporte creado con éxito.", "success")
        else:
            flash("Error al crear el reporte.", "danger")
        return redirect(url_for('reportes'))
    empleados = obtener_empleados()
    actividades = obtener_actividades()
    return render_template('reportes/form.html', reporte=None, empleados=empleados, actividades=actividades)

@app.route('/reportes/editar/<int:id>', methods=['GET', 'POST'])
def editar_reporte(id):
    reporte = obtener_reporte(id)
    if not reporte:
        flash("Reporte no encontrado.", "danger")
        return redirect(url_for('reportes'))

    if request.method == 'POST':
        id_empleado = request.form['id_empleado']
        id_actividad = request.form['id_actividad']
        
        # Convertir la cadena de fecha a objeto datetime
        fecha_str = request.form['fecha']
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
        except ValueError as e:
            flash(f"Formato de fecha u hora inválido: {e}", "danger")
            empleados = obtener_empleados()
            actividades = obtener_actividades()
            return render_template('reportes/form.html', reporte=reporte, empleados=empleados, actividades=actividades)

        acciones_realizadas = request.form['acciones_realizadas']
        comentarios = request.form['comentarios']
        porcentaje = request.form['porcentaje']
        entregable = request.form['entregable']
        estado = 'estado' in request.form
        
        if actualizar_reporte(id, id_empleado, id_actividad, fecha, acciones_realizadas, comentarios, porcentaje, entregable, estado):
            flash("Reporte actualizado con éxito.", "success")
        else:
            flash("Error al actualizar el reporte.", "danger")
        return redirect(url_for('reportes'))
    empleados = obtener_empleados()
    actividades = obtener_actividades()
    return render_template('reportes/form.html', reporte=reporte, empleados=empleados, actividades=actividades)

@app.route('/reportes/eliminar/<int:id>')
def eliminar_reporte_route(id):
    if eliminar_reporte(id):
        flash("Reporte eliminado con éxito.", "success")
    else:
        flash("Error al eliminar el reporte.", "danger")
    return redirect(url_for('reportes'))

if __name__ == '__main__':
    app.run(debug=True)