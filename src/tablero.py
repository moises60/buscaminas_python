import pygame
from celda import Celda
import random

class Tablero:
    def __init__(self, nivel, juego):
        """
        Argumentos:
            nivel (str): Nivel de dificultad seleccionado.
            juego (Juego): Referencia a la instancia del juego principal.
        Descripción:
            Inicializa el tablero de juego según el nivel de dificultad.
        """
        self.nivel = nivel
        self.juego = juego
        self.filas, self.columnas, self.minas = self.configurar_nivel(nivel)
        self.tamano_celda = 65  # Puedes ajustar el tamaño según tus preferencias
        self.juego_perdido = False
        self.juego_ganado = False
        self.primer_click = True
        self.celdas = [[Celda(fila, columna, self.tamano_celda, self) for columna in range(self.columnas)] for fila in range(self.filas)]
        # No generamos minas aquí; se generarán después del primer clic
        # self.generar_minas()
        # self.calcular_numeros()

    def configurar_nivel(self, nivel):
        """
        Argumentos:
            nivel (str): Nivel de dificultad.
        Descripción:
            Retorna la configuración de filas, columnas y minas según el nivel.
        """
        if nivel == 'Fácil':
            return 9, 9, 10
        elif nivel == 'Medio':
            return 14, 16, 30
        elif nivel == 'Difícil':
            return 14, 20, 59
        else:
            raise ValueError(f"Nivel desconocido: {nivel}")

    def generar_minas(self, excluir_celda=None):
        """
        Argumentos:
            excluir_celda (Celda): Celda a excluir de tener una mina.
        Descripción:
            Distribuye las minas aleatoriamente en el tablero, excluyendo una celda si se especifica.
        """
        posiciones_disponibles = [(f, c) for f in range(self.filas) for c in range(self.columnas)]
        if excluir_celda:
            posiciones_disponibles.remove((excluir_celda.fila, excluir_celda.columna))
            # Excluir también los vecinos inmediatos
            for vecino in excluir_celda.obtener_vecinos():
                posiciones_disponibles.remove((vecino.fila, vecino.columna))
        posiciones_minas = random.sample(posiciones_disponibles, self.minas)
        for fila, columna in posiciones_minas:
            self.celdas[fila][columna].tiene_mina = True

    def calcular_numeros(self):
        """
        Descripción:
            Calcula el número de minas adyacentes para cada celda.
        """
        for fila in range(self.filas):
            for columna in range(self.columnas):
                celda = self.celdas[fila][columna]
                if not celda.tiene_mina:
                    contador = self.contar_minas_adyacentes(fila, columna)
                    celda.numero = contador

    def contar_minas_adyacentes(self, fila, columna):
        """
        Argumentos:
            fila (int): Fila de la celda.
            columna (int): Columna de la celda.
        Descripción:
            Cuenta las minas adyacentes a una celda dada.
        """
        contador = 0
        for i in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for j in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if self.celdas[i][j].tiene_mina:
                    contador += 1
        return contador

    def manejar_evento(self, evento):
        """
        Argumentos:
            evento (pygame.event.Event): Evento de Pygame.
        Descripción:
            Maneja los eventos de entrada del jugador.
        """
        if not self.juego_perdido and not self.juego_ganado:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = evento.pos
                columna = pos_mouse[0] // self.tamano_celda
                fila = pos_mouse[1] // self.tamano_celda
                if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                    celda = self.celdas[fila][columna]
                    celda.manejar_evento(evento)

    def dibujar(self, pantalla):
        """
        Argumentos:
            pantalla (pygame.Surface): Superficie donde se dibuja el tablero.
        Descripción:
            Dibuja todas las celdas del tablero en la pantalla.
        """
        for fila in self.celdas:
            for celda in fila:
                celda.dibujar(pantalla)

    def actualizar(self):
        """
        Descripción:
            Actualiza el estado del tablero, revelando minas si el juego ha terminado.
        """
        if self.juego_perdido:
            tiempo_actual = pygame.time.get_ticks()
            if hasattr(self, 'celdas_minas_pendientes'):
                if self.indice_mina_actual < len(self.celdas_minas_pendientes):
                    if tiempo_actual - self.tiempo_ultima_revelacion > 200:  # Revelar cada 200 ms
                        celda_mina = self.celdas_minas_pendientes[self.indice_mina_actual]
                        celda_mina.revelada = True
                        # Reproducir sonido de explosión
                        self.juego.sonido_explosion.play()
                        self.indice_mina_actual += 1
                        self.tiempo_ultima_revelacion = tiempo_actual
        elif not self.juego_ganado:
            self.verificar_victoria()

    def preparar_revelacion_minas(self, celda_inicial):
        """
        Argumentos:
            celda_inicial (Celda): La celda donde se hizo clic y se encontró una mina.
        Descripción:
            Prepara la lista de minas para ser reveladas en orden de proximidad.
        """
        self.celdas_minas_pendientes = self.obtener_minas_ordenadas_por_distancia(celda_inicial)
        self.indice_mina_actual = 0
        self.tiempo_ultima_revelacion = pygame.time.get_ticks()

    def obtener_minas_ordenadas_por_distancia(self, celda_inicial):
        """
        Argumentos:
            celda_inicial (Celda): Celda desde la cual calcular las distancias.
        Descripción:
            Retorna una lista de celdas con minas ordenadas por distancia a la celda inicial.
        """
        celdas_mina = []
        for fila in self.celdas:
            for celda in fila:
                if celda.tiene_mina and celda != celda_inicial:
                    celdas_mina.append(celda)
        # Calcular distancia
        celdas_mina.sort(key=lambda celda: ((celda.fila - celda_inicial.fila)**2 + (celda.columna - celda_inicial.columna)**2))
        return celdas_mina

    def verificar_victoria(self):
        """
        Descripción:
            Verifica si todas las celdas sin minas han sido reveladas.
        """
        for fila in self.celdas:
            for celda in fila:
                if not celda.tiene_mina and not celda.revelada:
                    return  # Aún hay celdas por revelar
        # El jugador ha ganado
        self.juego_ganado = True
        # Reproducir sonido de victoria
        self.juego.sonido_victoria.play()
