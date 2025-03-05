from app import db, app
from models import Client

def clear_clients():
    with app.app_context():
        db.session.query(Client).delete()  # Elimina todos los registros
        db.session.commit()
        print("📌 Todos los clientes han sido eliminados.")

if __name__ == "__main__":
    clear_clients()