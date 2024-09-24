import pygame

class Interfaz:
    def __init__(self, pantalla):
        """
        Argumentos:
            pantalla (pygame.Surface): Superficie principal del juego.
        Descripción:
            Inicializa la interfaz gráfica del juego.
        """
        self.pantalla = pantalla
        self.fuente = pygame.font.SysFont("Arial", 24)
        self.tiempo_inicial = pygame.time.get_ticks()
        self.minas_restantes = 0

    def actualizar(self, tablero):
        """
        Argumentos:
            tablero (Tablero): Instancia del tablero de juego.
        Descripción:
            Actualiza y dibuja los elementos de la interfaz.
        """
        # Actualizar minas restantes
        marcadas = sum(celda.marcada for fila in tablero.celdas for celda in fila)
        self.minas_restantes = tablero.minas - marcadas

        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicial) // 1000
        texto_tiempo = self.fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, (0, 0, 0))
        texto_minas = self.fuente.render(f"Minas: {self.minas_restantes}", True, (0, 0, 0))

        pantalla_ancho, pantalla_alto = self.pantalla.get_size()
        self.pantalla.blit(texto_tiempo, (10, pantalla_alto - 40))
        self.pantalla.blit(texto_minas, (pantalla_ancho - 150, pantalla_alto - 40))
