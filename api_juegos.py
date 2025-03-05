import requests
from app import db, app
from models import Client

PEXELS_API_KEY = "Mlt11LB4vgM1Xeegfnq4vMolWzYRhznxUyTFBzJhX1l0UHq1lhigVq95"
PEXELS_URL = "https://api.pexels.com/v1/search"

def get_random_images(query="person", count=10):
    """ Obtiene múltiples imágenes de Pexels """
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": count}
    response = requests.get(PEXELS_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return [photo["src"]["medium"] for photo in data["photos"]] if data["photos"] else []
    return []

def populate_clients():
    """ Agrega nuevos clientes con imágenes aleatorias """
    clients_data = [
        {"name": "Carlos Pérez", "email": "carlos.perez@example.com"},
        {"name": "Mariana López", "email": "mariana.lopez@example.com"},
        {"name": "Alejandro Torres", "email": "alejandro.torres@example.com"},
        {"name": "Valeria Gómez", "email": "valeria.gomez@example.com"},
        {"name": "Santiago Ramírez", "email": "santiago.ramirez@example.com"},
    ]

    with app.app_context():
        image_urls = get_random_images(count=len(clients_data))
        
        for i, client in enumerate(clients_data):
            img_url = image_urls[i % len(image_urls)] if image_urls else "https://via.placeholder.com/150"
            new_client = Client(name=client["name"], email=client["email"], img_url=img_url)
            db.session.add(new_client)

        db.session.commit()
        print("✅ Clientes agregados correctamente.")

if __name__ == "__main__":
    populate_clients()
