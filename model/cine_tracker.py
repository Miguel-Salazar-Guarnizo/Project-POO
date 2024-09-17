import requests
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()


class TraktAPI:
    def __init__(self):
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.REDIRECT_URI = os.getenv('REDIRECT_URI')
        self.AUTH_URL = 'https://trakt.tv/oauth/authorize'
        self.TOKEN_URL = 'https://api.trakt.tv/oauth/token'
        self.API_URL = 'https://api.trakt.tv'
        self.access_token = None

    def authenticate(self):
        """Redirige al usuario a la URL de autorización y solicita el código de autorización."""
        authorization_url = f'{self.AUTH_URL}?response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}'
        webbrowser.open(authorization_url)
        auth_code = input('Introduce el código de autorización que obtuviste de Trakt: ')
        return self.get_access_token(auth_code)

    def get_access_token(self, auth_code):
        """Intercambia el código de autorización por un token de acceso."""
        data = {
            'code': auth_code,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        response = requests.post(self.TOKEN_URL, json=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            print(f"Access Token: {self.access_token}")
            return True
        else:
            print(f"Error al obtener el token: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False

    def get_watched_movies(self):
        """Obtiene las películas vistas por el usuario autenticado."""
        if not self.access_token:
            print("No tienes un access token. Autentica primero.")
            return []

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "trakt-api-version": "2",
            "trakt-api-key": self.CLIENT_ID
        }

        url = f"{self.API_URL}/sync/watched/movies"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener las películas vistas: {response.status_code}")
            return []


class User:
    def __init__(self, name, trakt_api):
        self.name = name
        self.trakt_api = trakt_api
        self.lists = {}

    def add_list(self, name_list, list):
        self.lists[name_list] = list

    def get_movies_viewed(self):
        """Obtiene y almacena las películas vistas del usuario en una lista."""
        watched_movies = self.trakt_api.get_watched_movies()
        if watched_movies:
            list_watched = List("Películas vistas")
            for item in watched_movies:
                movie = Movie(item['movie']['title'], item['movie']['year'])
                list_watched.add_movies(movie)
            self.add_list("Películas vistas", list_watched)

class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"{self.title} ({self.year})"


class List:
    def __init__(self, name):
        self.name = name
        self.movies = []

    def add_movies(self, movie: Movie):
        self.movies.append(movie)
