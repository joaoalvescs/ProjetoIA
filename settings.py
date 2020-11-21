import pygame
vec = pygame.math.Vector2

# configuracoes da tela
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

# ajuste de cores
BLACK = (0,0,0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255,255,255)

# configuracoes de fontes de texto
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# configs do jogador
#PLAYER_START_POS = 0
# mob configuracoes
