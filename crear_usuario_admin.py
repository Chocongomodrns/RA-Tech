from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuración de la app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://Chocongomodrns:Nubefrankland14@Chocongomodrns.mysql.pythonanywhere-services.com/Chocongomodrns$user"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo necesario
class clienteDatos(db.Model):
    __tablename__ = "clienteDatos"

    clienteId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellidos = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    correo = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='cliente')

with app.app_context():
    correo_a_promover = "modernslife@gmail.com"  # <-- CAMBIA ESTO POR EL CORREO DEL USUARIO

    usuario = clienteDatos.query.filter_by(correo=correo_a_promover).first()

    if usuario:
        usuario.rol = 'admin'
        db.session.commit()
        print(f"✅ El usuario {correo_a_promover} ha sido promovido a administrador.")
    else:
        print(f"❌ No se encontró ningún usuario con el correo: {correo_a_promover}")
