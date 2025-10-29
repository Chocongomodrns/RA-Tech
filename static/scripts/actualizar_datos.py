# CODIGO ACTUALIZAR DATOS PERFIL
from flask import redirect, request, url_for, session, flash

def actualizarDatosLog():
    from flask_app import db, clienteDatos, app

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    usuario = clienteDatos.query.get(usuario_id)
    if not usuario:
        flash("Usuario no encontrado.")
        return redirect(url_for('home'))

    usuario.nombre = request.form.get('nombre', '').strip() or None
    usuario.apellidos = request.form.get('apellidos', '').strip() or None
    usuario.direccion = request.form.get('direccion', '').strip() or None
    usuario.telefono = request.form.get('telefono', '').strip() or None

    try:
        db.session.commit()
        flash("Datos actualizados correctamente.")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al actualizar datos: {e}")
        flash("Hubo un error al actualizar los datos.")