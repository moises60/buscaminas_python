import pygame
from tablero import Tablero
from interfaz import Interfaz

class Juego:
    def __init__(self):
        """
        Descripción:
            Inicializa la clase Juego, configurando la ventana y el estado inicial.
        """
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Buscaminas")
        self.reloj = pygame.time.Clock()
        self.interfaz = None 
        self.ejecutando = True
        self.nivel = None
        self.tablero = None
        # sonidossss
        self.sonido_click = pygame.mixer.Sound('assets/sonidos/click.wav')
        self.sonido_explosion = pygame.mixer.Sound('assets/sonidos/explosion.wav')
        self.sonido_victoria = pygame.mixer.Sound('assets/sonidos/victoria.wav')

    def seleccionar_nivel(self):
        """
        Descripción:
            Muestra la pantalla de selección de nivel y establece el nivel elegido
        """
        fuente = pygame.font.SysFont("Arial", 36)
        opciones_nivel = ["Fácil", "Medio", "Difícil"]
        seleccionado = False
        boton_presionado = None

        while not seleccionado:
            self.pantalla.fill((255, 255, 255))
            titulo = fuente.render("SELECCIONA EL NIVEL DE DIFICULTAD", True, (0, 0, 0))
            self.pantalla.blit(titulo, (185, 100))

            # Dibujar botones para cada nivel
            botones = []
            for idx, nivel in enumerate(opciones_nivel):
                rect = pygame.Rect(300, 200 + idx * 70, 200, 50)
                
                # Si el botón está presionado, lo dibujamos con un color más oscuro
                if boton_presionado == nivel:
                    pygame.draw.rect(self.pantalla, (150, 150, 150), rect)  
                    texto_nivel = fuente.render(nivel, True, (0, 0, 0))
                    texto_rect = texto_nivel.get_rect(center=rect.center)
                    self.pantalla.blit(texto_nivel, texto_rect)
                else:
                    pygame.draw.rect(self.pantalla, (200, 200, 200), rect)  
                    texto_nivel = fuente.render(nivel, True, (0, 0, 0))
                    texto_rect = texto_nivel.get_rect(center=rect.center)
                    self.pantalla.blit(texto_nivel, texto_rect)

                botones.append((rect, nivel))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    self.sonido_click.play()
                    for rect, nivel in botones:
                        if rect.collidepoint(pos_mouse):
                            boton_presionado = nivel  
                elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    for rect, nivel in botones:
                        if rect.collidepoint(pos_mouse) and boton_presionado == nivel:
                            self.nivel = nivel
                            seleccionado = True
                    boton_presionado = None 

            self.reloj.tick(60)

    def ejecutar(self):
        """
        Descripción:
            Ejecuta el bucle principal del juego, manejando eventos y actualizando la pantalla.
        """
        self.seleccionar_nivel()
        self.tablero = Tablero(self.nivel, self)
        #  tamaño de la ventana
        ancho = self.tablero.columnas * self.tablero.tamano_celda
        alto = self.tablero.filas * self.tablero.tamano_celda + 50  
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.interfaz = Interfaz(self.pantalla)  # Actualizar  la interfaz

        fuente_mensaje = pygame.font.SysFont("Arial", 48)

        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False
                elif not self.tablero.juego_perdido and not self.tablero.juego_ganado:
                    self.tablero.manejar_evento(evento)
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    # Reiniciar el juego
                    self.__init__()  
                    self.ejecutar()
                    return

            self.pantalla.fill((255, 255, 255))
            self.tablero.actualizar()
            self.tablero.dibujar(self.pantalla)
            self.interfaz.actualizar(self.tablero)

            # Mostrar mensaje de fin de juego después de dibujar todo
            if self.tablero.juego_perdido:
                texto = fuente_mensaje.render("¡Has perdido! Pulsa 'R' para reiniciar.", True, (255, 0, 0))
                texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
                self.pantalla.blit(texto, texto_rect)
            elif self.tablero.juego_ganado:
                texto = fuente_mensaje.render("¡Has ganado! Pulsa 'R' para reiniciar.", True, (0, 255, 0))
                texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
                self.pantalla.blit(texto, texto_rect)

            pygame.display.flip()
            self.reloj.tick(60)
