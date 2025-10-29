# CODIGO LOGIN
from flask import redirect, request, url_for, session, flash, render_template
from werkzeug.security import check_password_hash

def loginLog(clienteDatos):
    """
    Procesa POST de login y devuelve una respuesta (redirect) si corresponde.
    Si es GET, devuelve None para que la vista principal renderice el formulario.
    """
    # Solo procesar cuando sea POST
    if request.method != 'POST':
        return None

    # Leer datos del formulario (con seguridad frente a KeyError)
    correo = request.form.get('correo', '').strip()
    password = request.form.get('password', '')

    if not correo or not password:
        flash('Ingresa correo y contraseña.')
        return redirect(url_for('login'))

    # Buscar al usuario por correo (AHORA dentro del POST, donde correo existe)
    user = clienteDatos.query.filter_by(correo=correo).first()

    if user and check_password_hash(user.password, password):
        session['usuario_id'] = user.clienteId
        session['usuario'] = user.nombre
        session['correo'] = user.correo
        session['rol'] = user.rol
        flash('Inicio de sesión con éxito.')
        return redirect(url_for('home'))
    else:
        flash('Correo o contraseña incorrectos.')
        return redirect(url_for('login'))
