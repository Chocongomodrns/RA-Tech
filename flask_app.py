# MI HOME

from flask import Flask, redirect, render_template, request, url_for

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)



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

db = SQLAlchemy(app)



class clienteDatos(db.Model):
    __tablename__ = "clienteDatos"

    clienteId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(4096))
    apellidos = db.Column(db.String(4096))
    direccion = db.Column(db.String(4096))
    correo = db.Column(db.String(4096))
    telefono = db.Column(db.String(4096))

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

class Proveedor(db.Model):
    __tablename__ = "Proveedor"
    idProveedor = db.Column(db.Integer, primary_key = True)
    nombreProveedor = db.Column(db.String(80))
    #Relacion
    articuloProveedor = db.relationship('articuloProveedor', back_populates="proveedor")

    def __repr__(self):
        return f'<Proveedor¿ {self.nombreProveedor}>'

class articuloVentas(db.Model):
    __tablename__ = "articuloVentas"
    idArticulo = db.Column(db.Integer, primary_key = True)
    nombreArticulo = db.Column(db.String(80))
    precioArticulo = db.Column(db.Float(2), nullable = True)
    stockArticulo = db.Column(db.Integer, nullable = True)
    #Relacion
    articulosProveedor = db.relationship('articuloProveedor', back_populates="articulo")

    def __repr__(self):
        return f'<Articulo¿ {self.nombreArticulo}>'

class articuloProveedor(db.Model):
    __tablename__ = "articuloProveedor"
    idArticuloProveedor = db.Column(db.Integer, primary_key = True)
    precioArticuloProveedor = db.Column(db.Float(2), nullable = True)
    nombreArticuloProveedor = db.Column(db.String(80))
    #Clave Foranea
    idProveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.idProveedor'), nullable = False)
    clienteId = db.Column(db.Integer, db.ForeignKey('articuloVentas.idArticulo'), nullable = False)
    #Relacion
    proveedor = db.relationship('Proveedor', back_populates="articuloProveedor")
    articulo = db.relationship('articuloVentas', back_populates="articulosProveedor")

    def __repr__(self):
        return f'<Articulo¿ {self.nombreArticuloProveedor}>'

@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/index", methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/registroCliente", methods = ["GET", "POST"])
def registroCliente():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidos = request.form.get("apellidos")
        direccion = request.form.get("direccion")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        # producto = request.form.get("producto")

        registro = clienteDatos(
            nombre = nombre,
            apellidos = apellidos,
            direccion = direccion,
            correo = correo,
            telefono = telefono
            )

        producto = clienteVenta (
            cliente = registro
            )

        db.session.add(registro)
        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template ('registroCliente.html')
