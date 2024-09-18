from typing import List
import requests
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()


class Auth:
    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str):
        self.CLIENT_ID: str = CLIENT_ID
        self.CLIENT_SECRET: str = CLIENT_SECRET
        self.REDIRECT_URI: str = REDIRECT_URI
        self.AUTH_URL: str = 'https://trakt.tv/oauth/authorize'
        self.TOKEN_URL: str = 'https://api.trakt.tv/oauth/token'
        self.API_URL: str = 'https://api.trakt.tv'
        self.access_token: str | None = None

    def authenticate(self) -> str:
        """Redirige al usuario a la URL de autorización y solicita el código de autorización."""
        authorization_url = f'{self.AUTH_URL}?response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}'
        webbrowser.open(authorization_url)
        auth_code = input('Introduce el código de autorización que obtuviste de Trakt: ')
        return self.get_access_token(auth_code)

    def get_access_token(self, auth_code: str) -> str | None:
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
            return self.access_token
        else:
            print(f"Error al obtener el token: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None


class TraktAPI:
    def __init__(self, CLIENT_ID: str, access_token: str = None):
        self.CLIENT_ID: str = CLIENT_ID
        self.API_URL: str = 'https://api.trakt.tv'
        self.access_token: str | None = access_token

    def get_headers(self) -> dict[str, str]:
        """Genera los headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "trakt-api-version": "2",
            "trakt-api-key": self.CLIENT_ID
        }

    def get_profile(self) -> dict[str, str] | None:
        """Obtiene la información del perfil del usuario autenticado."""
        if not self.access_token:
            print("No tienes un access token. Autentica primero.")
            return None
        headers = self.get_headers()

        url = f"{self.API_URL}/users/me"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Retorna el perfil del usuario
        else:
            print(f"Error al obtener el perfil: {response.status_code}")
            return None

    def get_watched_movies(self) -> dict[str, str] | list:
        """Obtiene las películas vistas por el usuario autenticado."""
        if not self.access_token:
            print("No tienes un access token. Autentica primero.")
            return []

        headers = self.get_headers()

        url = f"{self.API_URL}/sync/watched/movies"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener las películas vistas: {response.status_code}")
            return []

    def get_watch_list(self) -> list[dict[str, str]]:
        """Obtiene la lista de seguimiento del usuario."""
        if not self.access_token:
            print("No tienes un access token. Autentica primero.")
            return []

        headers = self.get_headers()
        url = f"{self.API_URL}/sync/watchlist/movies"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Lista de diccionarios con las películas en la lista de seguimiento
        else:
            print(f"Error al obtener la lista de seguimiento: {response.status_code}")
            return []


class User:
    def __init__(self, name: str, trakt_api: TraktAPI):
        self.name: str = name
        self.trakt_api: TraktAPI = trakt_api
        self.lists: dict[str, List] = {}

    def add_list(self, name_list: str, list: List):
        self.lists[name_list]: list[List] = list

    def get_movies_viewed(self):
        """Obtiene y almacena las películas vistas del usuario en una lista."""
        watched_movies = self.trakt_api.get_watched_movies()
        if watched_movies:
            list_watched = MovieList("Películas vistas")
            for item in watched_movies:
                movie = Movie(item['movie']['title'], item['movie']['year'])
                list_watched.add_movie(movie)
            self.add_list("Películas vistas", list_watched)

    def get_watch_list(self):
        """Obtiene la lista de seguimiento de películas."""
        watch_list = self.trakt_api.get_watch_list()
        if watch_list:
            watchlist = MovieList("Lista de seguimiento")  # Usa List en lugar de MovieList
            for item in watch_list:  # Itera sobre `watch_list` y no sobre `watchlist`
                movie = Movie(item['movie']['title'], item['movie']['year'])
                watchlist.add_movie(movie)
            self.add_list("Lista de seguimiento", watchlist)

    def show_lists(self):
        """Muestra todas las listas del usuario."""
        for list_name, list in self.lists.items():
            print(f"\nLista: {list_name}")
            list.show_movies()


class Movie:
    def __init__(self, title: str, year: str):
        self.title: str = title
        self.year: str = year

    def __str__(self):
        return f"{self.title} ({self.year})"


class MovieList:
    def __init__(self, name: str):
        self.name: str = name
        self.movies: list[Movie] = []

    def add_movie(self, movie: Movie):
        self.movies.append(movie)

    def show_movies(self):
        """Muestra las películas almacenadas en la lista."""
        if not self.movies:
            print("No hay películas en la lista.")
        for movie in self.movies:
            print(movie)
