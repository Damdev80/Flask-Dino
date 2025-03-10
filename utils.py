# utils.py
import requests




#Api para enviar la contraseña al correo

RESEND_API_KEY = "re_PMRFeK5e_Frar3AAJKYqiurVcrCy7MvLu"

def send_recovery_email(email, reset_url):
    url = "https://api.resend.com/emails"

    data = {
        "from": "onboarding@resend.dev",  # Dirección temporal de prueba
        "to": [email],  # Debe ser un correo real, como tu Gmail
        "subject": "Recuperación de contraseña",
        "html": f"""
            <h2>Restablecer contraseña</h2>
            <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
            <a href="{reset_url}">{reset_url}</a>
            <p>Si no solicitaste esto, ignora este mensaje.</p>
        """
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
