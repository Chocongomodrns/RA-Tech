from flask import redirect, request, url_for, session, flash, render_template

def verCarritoLog(carrito, productos, total_general):
    from flask_app import articuloVentas
    for id_articulo, cantidad in carrito.items():
        articulo = articuloVentas.query.get(int(id_articulo))
        if articulo:
            subtotal = articulo.precioArticulo * cantidad
            total_general += subtotal
            productos.append({
                'id': articulo.idArticulo,
                'nombre': articulo.nombreArticulo,
                'precio': articulo.precioArticulo,
                'cantidad': cantidad,
                'subtotal': subtotal,
                'imagen': articulo.imagen
            })
    return render_template('carrito.html', productos=productos, total_general=total_general)

