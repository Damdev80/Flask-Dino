from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)


#Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/dino_games_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Usuario que compró
    game_id = db.Column(db.String(50), nullable=False)  # ID del juego en la API
    game_title = db.Column(db.String(100), nullable=False)  # Título del juego
    price = db.Column(db.Float, nullable=False)  # Precio en el momento de la compra
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp())  # Fecha de compra


def save_purchase(user_id, game_data):
    hypothetical_price = round(random.uniform(10, 60), 2)  # Precio aleatorio entre 10 y 60

    new_purchase = Purchase(
        user_id=user_id,
        game_id=game_data["id"],
        game_title=game_data["title"],
        price=hypothetical_price  # Precio ficticio
    )
    db.session.add(new_purchase)
    db.session.commit()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/recover')
def recover_password():
    return render_template('recover.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')