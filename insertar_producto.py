from flask_app import db
from flask_app.models import articuloVentas

# Crear un nuevo producto
nuevo_producto = articuloVentas(
    nombreArticulo="Procesador Intel Core i5",
    precioArticulo=3500.00,
    stockArticulo=20,
    imagen="procesador_i5.png"  # Debes tener esta imagen en /static/img/
)

# Agregar a la base de datos
db.session.add(nuevo_producto)
db.session.commit()

print("Producto insertado con éxito.")