# ---------------------------- MI HOME ------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# ---------------------------- LIBRERIAS ----------------------------------------------------------------------------------

from flask import Flask, redirect, render_template, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# ---------------------------- DESFRAGMENTACION DE SCRIPTS ----------------------------------------------------------------

from static.scripts.agregar_producto import agregarProductoLog
from static.scripts.registro_cliente import registroClienteLog
from static.scripts.actualizar_datos import actualizarDatosLog
from static.scripts.mi_perfil import miPerfilLog
from static.scripts.login import loginLog
from static.scripts.ver_carrito import verCarritoLog
from static.scripts.checkout import checkoutLog

# -------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'Nubefrankland14'

app.config["DEBUG"] = True
app.app_context().push()

# -------------------------------------------------------------------------------------------------------------------------

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Chocongomodrns",
    password="Nubefrankland14",
    hostname="Chocongomodrns.mysql.pythonanywhere-services.com",
    databasename="Chocongomodrns$user",
)

# -------------------------------------------------------------------------------------------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}

# -------------------------------------------------------------------------------------------------------------------------

db = SQLAlchemy(app)

# -------------------------------------------------------------------------------------------------------------------------
# ---------------------------- TABLAS BASE DE DATOS -----------------------------------------------------------------------
class clienteDatos(db.Model):
    __tablename__ = "clienteDatos"
    # ------------------------------------------------------------------
    clienteId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellidos = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    correo = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable = False, default='cliente')
    # ------------------------------------------------------------------
    # -------------- RELACION FORANEA -------------------------------
    ventas = db.relationship("clienteVenta", back_populates="cliente")
    # ------------------------------------------------------------------
    def __repr__(self):
        return f'<clienteRATech {self.nombre}>'

class clienteVenta(db.Model):
    __tablename__ = "clienteVenta"
    # ------------------------------------------------------------------
    ventaId = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, db.ForeignKey('clienteDatos.clienteId'), nullable=False)
    producto = db.Column(db.String(80), nullable=True)
    cantidad = db.Column(db.Integer, default=1)
    precioUnitario = db.Column(db.Float(2), nullable=True)
    total = db.Column(db.Float(2), nullable=True)
    fecha = db.Column(db.DateTime, server_default=db.func.now())
    # ------------------------------------------------------------------
    cliente = db.relationship('clienteDatos', back_populates="ventas")

class articuloVentas(db.Model):
    __tablename__ = "articuloVentas"
    # ------------------------------------------------------------------
    idArticulo = db.Column(db.Integer, primary_key=True)
    nombreArticulo = db.Column(db.String(80))
    precioArticulo = db.Column(db.Float(2), nullable=True)
    stockArticulo = db.Column(db.Integer, nullable=True)
    imagen = db.Column(db.String(255))  # Nuevo campo para el nombre de archivo
    # ------------------------------------------------------------------
    def __repr__(self):
        return f'<Articulo¿ {self.nombreArticulo}>'

class historialVentas(db.Model):
    __tablename__ = "historialVentas"

    id = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, db.ForeignKey('clienteDatos.clienteId'), nullable=False)
    producto = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precioUnitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.func.now())

    cliente = db.relationship('clienteDatos', backref='historial')

# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------- RUTAS DE APP ---------------------------------------------------------------------------------

@app.route("/", methods = ["GET", "POST"])
def home():
    productos = articuloVentas.query.all()
    return render_template('home.html', productos=productos)

# -----------------------------------------------------------------------------------

@app.route("/login", methods = ["GET", "POST"])
def login():
    resultado = loginLog(clienteDatos)
    if resultado:
        return resultado

    return render_template('loginCliente.html')

# -----------------------------------------------------------------------------------

@app.route("/logout")
def logout():
    session.clear()
    flash('Sesion cerrada.')
    return redirect(url_for('home'))

# -----------------------------------------------------------------------------------

@app.route("/miPerfil", methods = ["GET", "POST"])
def miPerfil():
    resultado = miPerfilLog()
    if resultado:
        return resultado

    return redirect(url_for('login'))

# -----------------------------------------------------------------------------------

@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
    resultado = actualizarDatosLog()
    if resultado:
        return resultado

    return redirect(url_for('miPerfil'))

# -----------------------------------------------------------------------------------

@app.route("/index", methods = ["GET", "POST"])
def index():
    return render_template('index.html')

# -----------------------------------------------------------------------------------

@app.route("/registroCliente", methods = ["GET", "POST"])
def registroCliente():
    resultado = registroClienteLog()
    if resultado:
        return resultado
    return render_template ('registroCliente.html')

# -----------------------------------------------------------------------------------

@app.route("/agregarProducto", methods=["GET", "POST"])
def agregarProducto():
    resultado = agregarProductoLog()
    if resultado:
        return resultado

    return render_template("agregarProducto.html")

# -----------------------------------------------------------------------------------

@app.route('/historial')
def ver_historial():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para ver tu historial", "warning")
        return redirect(url_for('login'))

    cliente_id = session['usuario_id']

    # Traer todos los registros del historial del usuario
    historial = historialVentas.query.filter_by(clienteId=cliente_id).order_by(historialVentas.id.desc()).all()

    return render_template('historial.html', historial=historial)

# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------- CARRITO DE COMPRAS ---------------------------------------------------------------------------

def obtener_carrito():
    return session.get('carrito', {})

def guardar_carrito(carrito):
    session['carrito'] = carrito
    session.modified = True

# -----------------------------------------------------------------------------------

@app.route('/carrito')
def ver_carrito():
    carrito = obtener_carrito()
    productos = []
    total_general = 0

    resultado = verCarritoLog(carrito, productos, total_general)
    if resultado:
        return resultado

    return render_template('home')

# -----------------------------------------------------------------------------------

@app.route('/carrito/agregar/<int:id_articulo>', methods=['POST'])
def agregar_al_carrito(id_articulo):
    carrito = obtener_carrito()
    cantidad = int(request.form.get('cantidad', 1))
    carrito[str(id_articulo)] = carrito.get(str(id_articulo), 0) + cantidad
    guardar_carrito(carrito)
    flash('Producto añadido al carrito 🛒')
    return redirect(url_for('home'))


@app.route('/carrito/eliminar/<int:id_articulo>', methods=['POST'])
def eliminar_del_carrito(id_articulo):
    carrito = obtener_carrito()
    carrito.pop(str(id_articulo), None)
    guardar_carrito(carrito)
    flash('Producto eliminado del carrito ❌')
    return redirect(url_for('ver_carrito'))


@app.route('/carrito/vaciar')
def vaciar_carrito():
    session.pop('carrito', None)
    flash('Carrito vaciado 🧹')
    return redirect(url_for('ver_carrito'))

# -----------------------------------------------------------------------------------

@app.route('/carrito/checkout', methods=['GET', 'POST'])
def checkout():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para finalizar la compra.', 'warning')
        return redirect(url_for('login'))

    resultado = checkoutLog()
    if resultado:
        return resultado

# -----------------------------------------------------------------------------------

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()