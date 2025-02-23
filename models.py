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


# Modelo de Compra
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, nullable=False)
    game_title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Modelo de Juegos
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, image_url, price):
        self.name = name
        self.image_url = image_url
        self.price = price