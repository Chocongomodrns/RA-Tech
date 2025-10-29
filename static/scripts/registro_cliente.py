# REGISTRO CLIENTES

from flask import redirect, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

def registroClienteLog():
    from flask_app import db, clienteDatos

    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        # Evitar registros duplicados
        if clienteDatos.query.filter_by(correo=correo).first():
            flash('Este correo ya está registrado.')
            return redirect(url_for('registroCliente'))

        #Hashear la Contraseña
        password_hash = generate_password_hash(password)

        # Crear registro cliente
        registro = clienteDatos(
            correo = correo,
            password = password_hash
        )

        db.session.add(registro)
        db.session.commit()

        return redirect(url_for('login'))   # Redirigir al Login