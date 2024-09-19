import os
import sys

from model.code import TraktAPI, User, Movie, List, Auth


class UIConsole:

    def __init__(self):
        self.auth = Auth(CLIENT_ID=os.getenv('CLIENT_ID'),
                         CLIENT_SECRET=os.getenv('CLIENT_SECRET'),
                         REDIRECT_URI=os.getenv('REDIRECT_URI')
                         )
        self.trakt_api = None
        self.user = None
        self.options = {
            '1': self.authenticate_user,
            '2': self.show_watched_movies,
            '3': self.show_watch_list,
            '4': self.show_trend_movies,
            '0': self.exit
        }

    def print_menu(self):
        """Imprime el menú de la consola, incluyendo el nombre del usuario si está autenticado."""
        print("====================================")
        if self.user:  # Si el usuario está autenticado
            print(f'Trakt App Menu ({self.user.name})')  # Mostrar el nombre del usuario autenticado
        else:
            print('Trakt App Menu (No autenticado)')  # Si no está autenticado, indicar "No autenticado"
        print('1. Autenticar usuario')
        print('2. Ver películas vistas')
        print('3. Ver lista de seguimiento')
        print('4. Ver películas en tendencia')
        print('0. Salir')
        print("====================================")

    def run(self):
        while True:
            self.print_menu()
            option = input('Elige una opción: ')
            action = self.options.get(option)
            if action:
                action()
            else:
                print('Opción inválida')

    def authenticate_user(self):
        """Autentica al usuario y obtiene su perfil desde Trakt."""
        print(">>> Autenticando usuario ========================")
        access_token = self.auth.authenticate()
        if access_token:  # Intentamos autenticar al usuario
            self.trakt_api = TraktAPI(self.auth.CLIENT_ID, access_token)
            profile = self.trakt_api.get_profile()  # Obtenemos el perfil del usuario
            if profile:
                # Obtenemos el username del perfil o 'Usuario' si no está disponible
                user_name = profile.get('username', 'Usuario')
                # Creamos un nuevo objeto `User` con el nombre del usuario
                self.user = User(user_name, self.trakt_api)
                print(f"Autenticación exitosa. Bienvenido, {user_name}")
                input("Enter para continuar")
            else:
                print("Error al obtener el perfil del usuario.")
        else:
            print("Fallo en la autenticación")

    def show_watched_movies(self):
        """Muestra las películas vistas por el usuario autenticado."""
        if not self.user:  # Si el usuario no está autenticado
            print("Primero debes autenticar al usuario")
            return

        print(">>> Películas vistas ========================")
        self.user.get_movies_viewed()  # Llamamos al método para obtener las películas vistas
        self.user.show_lists("Películas vistas")  # Mostramos las listas del usuario
        input("===Enter para continuar===")

    def show_watch_list(self):
        if not self.user:
            print("Primero debes autenticar al usuario")
            return

        print(">>> Lista de seguimiento ========================")
        self.user.get_watch_list()
        self.user.show_lists("Lista de seguimiento")
        input("===Enter para continuar===")

    def show_trend_movies(self):
        if not self.user:
            print("Primero debes autenticar al usuario")
            return

        print(">>> Lista de películas en tendencia ========================")
        self.user.get_trend_movies()
        self.user.show_lists("Películas en tendencia")
        input("===Enter para continuar===")


    def exit(self):
        """Cierra la aplicación."""
        print("\n¡Adiós!")
        sys.exit(0)  # Salimos del programa


if __name__ == '__main__':
    ui = UIConsole()
    ui.run()
