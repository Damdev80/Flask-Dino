import requests
import random
from app import db, app
from models import Game


API_KEY = "7f1803aa44754a86862da2c0715ca900"
BASE_URL = "https://api.rawg.io/api/games"

def get_games_from_api():
    """Obtiene juegos desde la API y los guarda en la base de datos"""
    with app.app_context():  # ⚠️ Activar el contexto de la aplicación
        url = f"{BASE_URL}?key={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for game in data.get("results", []):
                name = game["name"]
                image_url = game.get("background_image", "")  # Algunos juegos pueden no tener imagen
                price = round(random.uniform(10, 60), 2)  # Genera un precio aleatorio

                # Verificar si el juego ya está en la base de datos
                existing_game = Game.query.filter_by(name=name).first()
                if not existing_game:
                    new_game = Game(name=name, image_url=image_url, price=price)
                    db.session.add(new_game)

            db.session.commit()
            print("Juegos guardados en la base de datos.")
        else:
            print("Error al obtener los juegos:", response.status_code)



# Para probarlo manualmente
if __name__ == "__main__":
    get_games_from_api()