# CODIGO CHECKOUT
from flask import redirect, request, url_for, session, flash, render_template

def checkoutLog():
    from flask_app import obtener_carrito, clienteDatos, articuloVentas, clienteVenta, db, historialVentas
    if request.method == 'POST':
        carrito = obtener_carrito()
        cliente_id = session['usuario_id']
        cliente = clienteDatos.query.get(cliente_id)
        total_general = 0

        for id_articulo, cantidad in carrito.items():
            articulo = articuloVentas.query.get(int(id_articulo))
            if articulo:
                subtotal = articulo.precioArticulo * cantidad
                total_general += subtotal

                venta = clienteVenta(
                    clienteId=cliente.clienteId,
                    producto=articulo.nombreArticulo,
                    cantidad=cantidad,
                    precioUnitario=articulo.precioArticulo,
                    total=subtotal
                )
                db.session.add(venta)

                # Guardar en historial de ventas
                historial = historialVentas(
                    clienteId=cliente.clienteId,
                    producto=articulo.nombreArticulo,
                    cantidad=cantidad,
                    precioUnitario=articulo.precioArticulo,
                    total=subtotal
                )
                db.session.add(historial)

                # opcional: restar stock
                #if articulo.stockArticulo is not None:
                #    articulo.stockArticulo = max(0, articulo.stockArticulo - cantidad)

        db.session.commit()
        session.pop('carrito', None)
        flash(f'Compra realizada con éxito. Total: ${total_general:.2f}', 'success')
        # Redirigir a página de confirmación
        return render_template('confirmacion.html', total_general=total_general)

    carrito = obtener_carrito()
    productos = []
    total_general = 0
    for id_articulo, cantidad in carrito.items():
        articulo = articuloVentas.query.get(int(id_articulo))
        if articulo:
            subtotal = articulo.precioArticulo * cantidad
            total_general += subtotal
            productos.append({
                'nombreArticulo': articulo.nombreArticulo,
                'precioUnitario': articulo.precioArticulo,
                'cantidad': cantidad,
                'total': subtotal
            })
    return render_template('checkout.html', productos=productos, total_general=total_general)