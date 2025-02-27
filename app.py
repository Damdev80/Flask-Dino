from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Game  # Asegúrate de importar el modelo User desde models.py
from utils import send_recovery_email
from datetime import datetime, timedelta, timezone
import os, secrets


app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/dino_games_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.urandom(24)

# Inicializamos LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # Asegúrate de inicializar LoginManager con la app
login_manager.login_view = 'login'  # Aquí indicamos la vista de login por defecto

# Inicializamos SQLAlchemy
db.init_app(app)  

# Cargador de usuario necesario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Recupera el usuario de la base de datos

# Página de inicio (solo accesible para usuarios registrados)
@app.route('/')
@login_required
def index():
    return render_template('index.html'), 404
    

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')

    return render_template('login.html')

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('¡Te has registrado exitosamente!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta para la recuperación de contraseña (si decides implementarla)
@app.route('/recover', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Generar token seguro
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
            db.session.commit()

            # URL de recuperación
            reset_url = url_for('reset_password', token=token, _external=True)

            # Enviar el correo con Resend
            response = send_recovery_email(email, reset_url)

            if response.get("error"):
                flash("Error al enviar el correo. Intenta más tarde.", "error")
            else:
                flash("Se ha enviado un enlace de recuperación a tu correo.", "success")
        else:
            flash("No se encontró una cuenta con ese email.", "error")

    return render_template('recover.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_expiration < datetime.utcnow():
        flash("El enlace ha expirado o es inválido.", "error")
        return redirect(url_for('recover_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not confirm_password:
            flash("El campo de confirmación es obligatorio.", "error")
            return redirect(request.url)
        
        if new_password != confirm_password:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for('reset_password', token=token))

        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        user.password = hashed_password
        user.reset_token = None
        user.reset_expiration = None
        db.session.commit()

        flash("Tu contraseña ha sido restablecida con éxito. Inicia sesión.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)



#Ruta para mostrar coleccion de juegos
@app.route('/categorias')
def categorias():
    juegos = Game.query.all()
    return render_template('categorias.html', juegos=juegos)

@app.route('/bienvenido')
def welcome():
    return render_template('welcome.html')

@app.route('/api/juegos')
def api_juegos():
    juegos = Game.query.all()
    juegos_json = [{"id": j.id, "name": j.name, "image_url": j.image_url, "price": j.price, "genre": j.genre} for j in juegos]
    return jsonify(juegos_json)

# Crear las tablas de la base de datos (dentro del contexto de la aplicación)
with app.app_context():
    db.create_all()  
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
