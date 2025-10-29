# CODIGO MI PERFIL
from flask import redirect, request, url_for, session, flash, render_template

def miPerfilLog():
    from flask_app import db, clienteDatos, app

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash("No has iniciado sesión.")
        return redirect(url_for('login'))

    try:
        usuario = clienteDatos.query.filter_by(clienteId=usuario_id).first()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al acceder al perfil: {e}")
        flash("Error de conexión a la base de datos.")
        return redirect(url_for('inicio'))
    if not usuario:
        flash("Usuario no encontrado.")
        return redirect(url_for('login'))

    return render_template('miPerfil.html',
                           nombre=usuario.nombre,
                            apellidos=usuario.apellidos,
                            telefono=usuario.telefono,
                            direccion=usuario.direccion,
                            correo=usuario.correo)