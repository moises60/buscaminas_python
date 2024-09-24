import pygame

class Celda:
    def __init__(self, fila, columna, tamano_celda, tablero):
        """
        Argumentos:
            fila (int): Fila de la celda en el tablero.
            columna (int): Columna de la celda en el tablero.
            tamano_celda (int): Tamaño de la celda en píxeles.
            tablero (Tablero): Referencia al tablero al que pertenece la celda.
        Descripción:
            Inicializa una celda con sus propiedades predeterminadas.
        """
        self.fila = fila
        self.columna = columna
        self.tamano_celda = tamano_celda
        self.tablero = tablero
        self.tiene_mina = False
        self.revelada = False
        self.marcada = False
        self.numero = 0
        self.rect = pygame.Rect(columna * tamano_celda, fila * tamano_celda, tamano_celda, tamano_celda)

        # Cargar imágenes 
        self.imagen_celda_oculta = pygame.transform.scale(pygame.image.load('assets/imagenes/celda.png'), (tamano_celda, tamano_celda))
        self.imagen_bandera = pygame.transform.scale(pygame.image.load('assets/imagenes/bandera.png'), (tamano_celda, tamano_celda))
        self.imagen_mina = pygame.transform.scale(pygame.image.load('assets/imagenes/mina.png'), (tamano_celda, tamano_celda))
        self.imagenes_numeros = [pygame.transform.scale(pygame.image.load(f'assets/imagenes/numeros/{i}.png'), (tamano_celda, tamano_celda)) for i in range(1, 5)]

    def revelar(self):
        """
        Descripción:
            Revela la celda y, si es necesario, revela las celdas adyacentes.
        """
        if not self.revelada and not self.marcada:
            if self.tablero.primer_click:
                self.tablero.primer_click = False
                self.tablero.generar_minas(excluir_celda=self)
                self.tablero.calcular_numeros()
            self.revelada = True
            if self.tiene_mina:
                # Reproducir sonido de explosión
                self.tablero.juego.sonido_explosion.play()
                # Manejar condición de pérdida
                self.tablero.juego_perdido = True
                self.tablero.preparar_revelacion_minas(self)
            else:
                # Reproducir sonido de clic
                self.tablero.juego.sonido_click.play()
                if self.numero == 0:
                    self.revelar_adyacentes()

    def revelar_adyacentes(self):
        """
        Descripción:
            Revela recursivamente las celdas adyacentes sin minas.
        """
        for vecino in self.obtener_vecinos():
            if not vecino.revelada and not vecino.tiene_mina:
                vecino.revelar()

    def obtener_vecinos(self):
        """
        Descripción:
            Obtiene una lista de celdas vecinas.
        """
        vecinos = []
        for i in range(max(0, self.fila - 1), min(self.tablero.filas, self.fila + 2)):
            for j in range(max(0, self.columna - 1), min(self.tablero.columnas, self.columna + 2)):
                if i == self.fila and j == self.columna:
                    continue
                vecinos.append(self.tablero.celdas[i][j])
        return vecinos

    def dibujar(self, pantalla):
        """
        Argumentos:
            pantalla (pygame.Surface): Superficie donde se dibuja la celda.
        Descripción:
            Dibuja la celda en la pantalla según su estado.
        """
        if self.revelada:
            if self.tiene_mina:
                pantalla.blit(self.imagen_mina, self.rect)
            elif self.numero > 0:
                pantalla.blit(self.imagenes_numeros[self.numero - 1], self.rect)
            else:
                # Celda vacía revelada
                pygame.draw.rect(pantalla, (200, 200, 200), self.rect)
        else:
            if self.marcada:
                pantalla.blit(self.imagen_bandera, self.rect)
            else:
                pantalla.blit(self.imagen_celda_oculta, self.rect)

    def manejar_evento(self, evento):
        """
        Argumentos:
            evento (pygame.event.Event): Evento de Pygame.
        Descripción:
            Maneja los eventos específicos de la celda.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if evento.button == 1:  # Clic izquierdo
                    self.revelar()
                elif evento.button == 3:  # Clic derecho
                    self.marcada = not self.marcada
