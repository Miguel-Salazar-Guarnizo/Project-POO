import requests
import time
from dotenv import load_dotenv
import os
import webbrowser

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
AUTH_URL = 'https://trakt.tv/oauth/authorize'
TOKEN_URL = 'https://api.trakt.tv/oauth/token'
LIST_URL = 'https://api.trakt.tv/users/{username}/lists/{listname}/items'
API_URL = 'https://api.trakt.tv'

# Paso 1: Redirigir al usuario para que autorice y obtener el código de autorización

# Abrir la URL de autorización en el navegador
authorization_url = f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
webbrowser.open(authorization_url)

# Pedir al usuario que ingrese el código de autorización
auth_code = input('Introduce el código de autorización que obtuviste de Trakt: ')

# Paso 2: Intercambiar el código de autorización por un access_token
data = {
    'code': auth_code,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code',
}

response = requests.post(TOKEN_URL, json=data)
token_data = response.json()
access_token = token_data['access_token']

if response.status_code == 200:
    print(f"Access Token: {token_data['access_token']}")
    print(f"Refresh Token: {token_data['refresh_token']}")
else:
    print(f"Error al obtener el token: {response.status_code}")
    print(f"Respuesta: {token_data}")
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