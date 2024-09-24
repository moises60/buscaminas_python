import pygame
from juego import Juego

def main():
    """
    Descripción:
        Punto de entrada principal del juego. Inicializa Pygame y crea una instancia de Juego.
    """
    pygame.init()
    pygame.mixer.init()  # Inicializar el mezclador de sonidos
    juego = Juego()
    juego.ejecutar()
    pygame.quit()

if __name__ == "__main__":
    main()
