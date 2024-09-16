import requests
import time
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_URL = 'https://api.trakt.tv'

# Generar códigos de dispositivo
url = f"{API_URL}/oauth/device/code"
payload = {
    "client_id": CLIENT_ID
}

response = requests.post(url, data=payload)
data = response.json()

# Extraer los códigos
user_code = data['user_code']
device_code = data['device_code']
verification_url = data['verification_url']
expires_in = data['expires_in']
interval = data['interval']

print(f"Por favor, ve a {verification_url} e ingresa el código: {user_code}")

# Definir URL de token de dispositivo
url_token = f"{API_URL}/oauth/device/token"
payload_token = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": device_code
}

# Verificar la autorización
start_time = time.time()
access_token = None  # Para almacenar el access_token después de la autenticación exitosa

while time.time() - start_time < expires_in:
    response_token = requests.post(url_token, data=payload_token)

    # Verifica el código de estado antes de intentar convertir a JSON
    if response_token.status_code == 200:
        try:
            token_data = response_token.json()  # Intenta convertir a JSON
            access_token = token_data['access_token']
            refresh_token = token_data['refresh_token']
            print("¡Autenticación exitosa!")
            print(f"Access Token: {access_token}")
            break
        except requests.exceptions.JSONDecodeError:
            print("Error al decodificar la respuesta JSON.")
    else:
        print(f"Error: {response_token.status_code} - {response_token.text}")

    if response_token.status_code == 400:
        print("Código no autorizado aún. Intentando de nuevo...")
    elif response_token.status_code == 404:
        print("Código no encontrado o expirado.")
        break
    else:
        print(f"Error: {response_token.status_code}")

    time.sleep(interval)

# Si existe acces_token, se hace la solicitud para obtener las películas vistas
if access_token:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "trakt-api-version": "2",
        "trakt-api-key": CLIENT_ID
    }

    # Endpoint para obtener las películas vistas por el usuario
    url_watched_movies = f"{API_URL}/sync/watched/movies"

    response_watched_movies = requests.get(url_watched_movies, headers=headers)

    if response_watched_movies.status_code == 200:
        watched_movies = response_watched_movies.json()
        print("Películas vistas por el usuario:")

        for movie in watched_movies:
            print(f"Título: {movie['movie']['title']}, Año: {movie['movie']['year']}")
    else:
        print(f"Error al obtener las películas vistas: {response_watched_movies.status_code}")
else:
    print("No se pudo obtener un access token.")