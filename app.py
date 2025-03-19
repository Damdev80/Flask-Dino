from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Game, Client, Product, Empleado  # Asegúrate de importar el modelo User desde models.py
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
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@login_required
@app.route('/index')
def index():
    flash('¡Inicio de sesión exitoso!', 'success')
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

# Ruta para la recuperación de contraseña 
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


#Entorno de pruebas
@app.route('/test')
def test():
    return render_template('test.html')



#Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

@app.route('/dashboard/usuarios')
def usuarios():
    return render_template('usuarios.html')

#Modelo de juego y el CRUD
@app.route('/dashboard/categorias')
def categorias():
    juegos = Game.query.all()
    return render_template('categorias.html', juegos=juegos)


@app.route('/dashboard/categorias/nuevo', methods=['GET', 'POST'])
def new_games():
    if request.method == 'POST':
        name = request.form['name']
        image_url = request.form['image_url']
        price = float(request.form['price'])
        categoria = request.form['categoria']
        
        if Game.query.filter_by(name=name).first():
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('new_games')) 
        
        nuevo_juego = Game(name=name, image_url=image_url, price=price, categoria=categoria)
        db.session.add(nuevo_juego)
        db.session.commit()
        
        flash('Juego agregado correctamente.', 'success')
        return redirect(url_for('categorias'))

    return render_template('nuevo-juego.html')

@app.route('/dashboard/usuarios/', methods=['GET', 'POST'])
def clientes_show():
    usuarios = Client.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/api/clientes/')
def clientes():
    clients = Client.query.all()  
    clients_data = [
        { "id": client.id, "name": client.name, "email": client.email, "img_url": client.img_url }
        for client in clients
    ]  
    return jsonify(clients_data)

@app.route('/api/juegos')   
def api_juegos():
    juegos = Game.query.all()
    juegos_json = [{"id": j.id, "name": j.name, "image_url": j.image_url, "price": j.price, "genre": j.genre} for j in juegos]
    return jsonify(juegos_json)

#Modelo de usuarios y su CRUD
    
@app.route('/dashboard/usuario/', methods=['GET', 'POST'])
def show_usuario():
    usuario = User.query.all()
    return render_template('usuarios.html', usuario=usuario)

@app.route('/api/usuario', methods=['GET', 'POST'])
def api_usuario():
    usuario = User.query.all()
    usuario_json = [{"id": User.id, "username": User.username, "email": User.email} for User in usuario]
    return jsonify(usuario_json)

# Ruta para eliminar un usuario
@app.route('/dashboard/usuario/desactivar/<int:user_id>', methods=['POST'])
def desactivar_usuario(user_id):
    usuario = User.query.get(user_id)
    
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('dashboard'))  # Redirigir a donde tengas tu lista de usuarios

    usuario.is_active = False  # Cambiar el estado a inactivo
    db.session.commit()

    flash("Usuario desactivado correctamente", "success")
    return redirect(url_for('dashboard'))  # Redirigir a la lista de usuarios

# Ruta para actualizar un usuario
@app.route('/dashboard/usuario/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)  # Si no encuentra el usuario, devuelve un error 404

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        if username and email:  # Aseguramos que no sean valores vacíos
            usuario.username = username
            usuario.email = email
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('show_usuario'))
        else:
            flash('Todos los campos son obligatorios.', 'danger')

    return render_template('editar_usuario.html', usuario=usuario)



# Modelo de empleado  y su CRUD

@app.route('/dashboard/empleado/')
def show_empleado():
    empleados = Empleado.query.all()
    flash('Empleado agregado correctamente.', 'success')
    return render_template('empleado.html', empleados=empleados)

@app.route('/api/empleado', methods=['GET', 'POST'])
def api_empleado():
    empleados = Empleado.query.all()
    empleado_json = [{"id": Empleado.id, "name": Empleado.name, "email": Empleado.email, "phone": Empleado.phone, "address": Empleado.address, "job": Empleado.job} for Empleado in empleados]
    return jsonify(empleado_json)

@app.route('/dashboard/empleado/nuevo/')
def nuevo_empleado():
    
    return render_template('nuevo-empleado.html')

@app.route('/dashboard/empleado/nuevo/', methods=['POST'])
def crear_empleado():
    name = request.form['name']
    img_url = request.form['img_url']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    job = request.form['job']
    
    nuevo_empleado = Empleado(name=name, img_url=img_url, email=email, phone=phone, address=address, job=job)
    db.session.add(nuevo_empleado)
    db.session.commit()
    
    return redirect(url_for('show_empleado'))


# @app.route('/dashboard/empleado/editar/<int:id>', methods=['GET', 'POST'])
# def editar_empleado(id):
#     empleado = Empleado.query.get_or_404(id)  # Si no encuentra el usuario, devuelve un error 404

#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')

#         if name and email:  # Aseguramos que no sean valores vacíos
#             empleado.name = name
#             empleado.email = email
#             db.session.commit()
#             flash('Empleado actualizado correctamente.', 'success')
#             return redirect(url_for('show_empleado'))
#         else:
#             flash('Todos los campos son obligatorios.', 'danger')

#     return render_template('empleado.html', empleado=empleado)

# @app.route('/dashboard/empleado/editar/<int:id>', methods=['GET', 'POST'])
# def editar_empleado(id):
#     empleado = Empleado.query.get_or_404(id)  # Si no encuentra el usuario, devuelve un error 404

#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')

#         if name and email:  # Aseguramos que no sean valores vacíos
#             empleado.name = name
#             empleado.email = email
#             db.session.commit()
#             flash('Empleado actualizado correctamente.', 'success')
#             return redirect(url_for('show_empleado'))
#         else:
#             flash('Todos los campos son obligatorios.', 'danger')

#     return render_template('empleado.html', empleado=empleado)

#Modelo de productos
@app.route('/dashboard/productos/')
def show_productos():
    productos = Product.query.all()
    return render_template('productos.html', productos=productos)

@app.route('/api/productos')
def api_productos():
    productos = Product.query.all()
    productos_json = [{"id": Product.id, "name": Product.name, "img_url": Product.img_url, "price": Product.price, "stock": Product.stock} for Product in productos]
    return jsonify(productos_json)   


@app.route('/dashboard/productos/nuevo')
def nuevo_producto():
    return render_template("nuevo-producto.html")

@app.route('/dashboard/productos/nuevo', methods=['POST'])
def crear_producto():
    name = request.form['name']
    price = request.form['price']
    img_url = request.form['img_url']
    stock = request.form['stock']
    
    nuevo_producto = Product(name=name, price=price, img_url=img_url, stock=stock)
    db.session.add(nuevo_producto)
    db.session.commit()
    
    flash('Producto agregado correctamente.', 'success')
    return redirect(url_for('show_productos'))
    
# Crear las tablas de la base de datos (dentro del contexto de la aplicación)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
