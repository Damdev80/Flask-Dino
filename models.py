from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Solo defines la instancia de SQLAlchemy, no la inicializas

# Modelo de Usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    # Campos para la recuperación de contraseña
    reset_token = db.Column(db.String(100), nullable=True)
    reset_expiration = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



# Modelo de Juegos
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

    def __init__(self, name, image_url, price, categoria):
        self.name = name
        self.image_url = image_url
        self.price = price
        self.categoria = categoria
        
# Modelo de clientes
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
  
    def __init__(self, name, img_url, email):
        self.name = name
        self.img_url = img_url
        self.email = email
        
#Modelo de productos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    
    def __init__(self, name, img_url, price, stock):
        self.name = name
        self.img_url = img_url
        self.price = price
        self.stock = stock
        
#Modelo de empleados
class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    job = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, img_url, email, phone, address, job):
        self.name = name
        self.img_url = img_url
        self.email = email
        self.phone = phone
        self.address = address
        self.job = job
        