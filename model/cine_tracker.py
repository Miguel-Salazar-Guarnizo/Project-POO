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