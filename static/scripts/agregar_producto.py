# CODIGO AGREGAR PRODUCTO
from flask import redirect, request, url_for, session, flash

def agregarProductoLog():
    from flask_app import db, articuloVentas

    if session.get('rol') != 'admin':
            flash("Acceso denegado. Se requieren permisos de administrador.")
            return redirect(url_for('home'))

    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            precio = float(request.form["precio"])
            stock = int(request.form["stock"])
            imagen = request.form["imagen"]  # nombre del archivo, por ejemplo: "procesador.png"

            nuevo = articuloVentas(
                nombreArticulo=nombre,
                precioArticulo=precio,
                stockArticulo=stock,
                imagen=imagen
            )
            db.session.add(nuevo)
            db.session.commit()
            flash("Producto agregado con éxito.")
            return redirect(url_for('catalogo'))
        except Exception as e:
            db.session.rollback()
            flash("Error al guardar el producto: " + str(e))

    return None;