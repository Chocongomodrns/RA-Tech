# MI HOME

from flask import Flask, redirect, render_template, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'Nubefrankland14'


app.config["DEBUG"] = True

app.app_context().push()



SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(

    username="Chocongomodrns",

    password="Nubefrankland14",

    hostname="Chocongomodrns.mysql.pythonanywhere-services.com",

    databasename="Chocongomodrns$user",

)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}

db = SQLAlchemy(app)



class clienteDatos(db.Model):
    __tablename__ = "clienteDatos"

    clienteId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellidos = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    correo = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable = False, default='cliente')

    ventas = db.relationship("clienteVenta", back_populates="cliente")

    def __repr__(self):
        return f'<clienteRATech {self.nombre}>'

class clienteVenta(db.Model):
    __tablename__ = "clienteVenta"
    ventaId = db.Column(db.Integer, primary_key = True)
    #Clave Foranea
    clienteId = db.Column(db.Integer, db.ForeignKey('clienteDatos.clienteId'), nullable = False)
    producto = db.Column(db.String(80), nullable = True)
    #Relacion
    cliente = db.relationship('clienteDatos', back_populates="ventas")

    def __repr__(self):
        return f'<Venta¿ {self.producto}>'

class articuloVentas(db.Model):
    __tablename__ = "articuloVentas"
    idArticulo = db.Column(db.Integer, primary_key=True)
    nombreArticulo = db.Column(db.String(80))
    precioArticulo = db.Column(db.Float(2), nullable=True)
    stockArticulo = db.Column(db.Integer, nullable=True)
    imagen = db.Column(db.String(255))  # Nuevo campo para el nombre de archivo

    def __repr__(self):
        return f'<Articulo¿ {self.nombreArticulo}>'

@app.route("/", methods = ["GET", "POST"])
def home():
    productos = articuloVentas.query.all()
    return render_template('home.html', productos=productos)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        # Buscar al usuario por Correo
        user = clienteDatos.query.filter_by(correo=correo).first()

        if user and check_password_hash(user.password, password):
            session['usuario_id'] = user.clienteId
            session['usuario'] = user.nombre
            session['correo'] = user.correo
            session['rol'] = user.rol
            flash('Inicio de esión con exito.')
            return redirect(url_for('home'))
        else:
            flash('Correo o contraseña incorrectos.')

    return render_template('loginCliente.html')

@app.route("/logout")
def logout():
    session.clear()
    flash('Sesion cerrada.')
    return redirect(url_for('home'))

@app.route("/miPerfil", methods = ["GET", "POST"])
def miPerfil():
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

@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
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

    return redirect(url_for('miPerfil'))

@app.route("/index", methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/registroCliente", methods = ["GET", "POST"])
def registroCliente():
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

    return render_template ('registroCliente.html')

@app.route("/agregarProducto", methods=["GET", "POST"])
def agregarProducto():
    if session.get('rol') != 'admin':
        flash("Acceso denegado. Se requieren permisos de administrador.")
        return redirect(url_for('home'))

    if request.method == "POST":
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
        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Producto agregado con éxito.")
            return redirect(url_for('catalogo'))
        except Exception as e:
            db.session.rollback()
            flash("Error al guardar el producto: " + str(e))

    return render_template("agregarProducto.html")
