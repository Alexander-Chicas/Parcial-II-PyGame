import pygame
import sys

# Inicialización de PyGame
pygame.init()

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Primal geometry - PyGame')

# Definimos colores
BLANCO = (255, 255, 255)
AZUL = (0, 128, 255)
NEGRO = (0, 0, 0)

# Clase del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTO_PANTALLA - 100
        self.velocidad_y = 0
        self.velocidad_x = 0
        self.sobre_plataforma = False

    def saltar(self):
        if self.sobre_plataforma:
            self.velocidad_y = -15  # Salto

    def gravedad(self):
        if not self.sobre_plataforma:
            self.velocidad_y += 1  # Caída por gravedad
        if self.rect.y >= ALTO_PANTALLA - 60:
            self.rect.y = ALTO_PANTALLA - 60
            self.velocidad_y = 0
            self.sobre_plataforma = True

    def update(self):
        self.gravedad()
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x

# Clase de las plataformas
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Grupo de sprites
todos_los_sprites = pygame.sprite.Group()
plataformas = pygame.sprite.Group()

# Creamos al jugador
jugador = Jugador()
todos_los_sprites.add(jugador)

# Creamos plataformas
plataforma1 = Plataforma(0, ALTO_PANTALLA - 20, ANCHO_PANTALLA, 20)
plataforma2 = Plataforma(300, ALTO_PANTALLA - 150, 200, 20)
plataforma3 = Plataforma(500, ALTO_PANTALLA - 250, 200, 20)
plataformas.add(plataforma1, plataforma2, plataforma3)
todos_los_sprites.add(plataforma1, plataforma2, plataforma3)

# Bucle principal del juego
reloj = pygame.time.Clock()
while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.saltar()
            if event.key == pygame.K_LEFT:
                jugador.velocidad_x = -5
            if event.key == pygame.K_RIGHT:
                jugador.velocidad_x = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador.velocidad_x = 0

    # Actualizacion de los sprites
    todos_los_sprites.update()

    # aqui verificamos las coliciones en las plataformas
    colisiones = pygame.sprite.spritecollide(jugador, plataformas, False)
    if colisiones:
        jugador.sobre_plataforma = True
        jugador.rect.y = colisiones[0].rect.top - jugador.rect.height
        jugador.velocidad_y = 0
    else:
        jugador.sobre_plataforma = False

    # Dibujamos la pantalla
    screen.fill(BLANCO)
    todos_los_sprites.draw(screen)

    # Actualizamos la pantalla
    pygame.display.flip()

    # Control de frames por segundo
    reloj.tick(60)
