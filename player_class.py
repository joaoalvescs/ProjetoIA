import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
  def __init__(self, app, pos):
    self.app = app
    self.grid_pos = pos
    self.pix_pos = self.get_pix_pos()
    self.direction = vec(1,0)
    self.stored_direction = None
    self.able_to_move = True
    self.current_score = 0

    self.angle = -90 #Angulo inicial da sprite do Jogador (virada para a direita)
    self.last_key_pressed = 'right' #Direção inicial do Jogador sendo registrada como uma tecla pressionada
    self.PLAYER_SPRITE = pygame.image.load('./sprites/player.png').convert_alpha()
    self.PLAYER_SPRITE = pygame.transform.scale(self.PLAYER_SPRITE, (self.app.cell_width, self.app.cell_height))
    self.PLAYER_SPRITE = pygame.transform.rotate(self.PLAYER_SPRITE, self.angle)
 

  def update(self):
    if self.able_to_move:
      self.pix_pos += self.direction
    # Mover-se apenas dentro do grid
    if self.time_to_move():
        if self.stored_direction != None:
          self.direction = self.stored_direction
        self.able_to_move = self.can_move()
    # Configurando grid_pos em relação a pix_pos
    self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
    self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER+self.app.cell_height//2)//self.app.cell_height+1

    if self.on_coin():
      self.eat_coin()

  def draw(self, app):
    self.app = app
    #Inserindo o jogador na tela
    app.screen.blit(self.PLAYER_SPRITE, (int(self.pix_pos.x-10), int(self.pix_pos.y-10)))

    #Inserindo o retangulo referente a grid_pos
    pygame.draw.rect(self.app.screen, RED,
    (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
     self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, 
     self.app.cell_width, self.app.cell_height), 1)

  def on_coin(self):
    if self.grid_pos in self.app.coins:
      return True
    else:
      return False

  def eat_coin(self):
    self.app.coins.remove(self.grid_pos)
    self.current_score += 1

  def move(self, direction, angle):
    #Contem a direcao e o angulo, que vai ser usado para rotacionar a sprite
    self.stored_direction = direction
    self.PLAYER_SPRITE = pygame.transform.rotate(self.PLAYER_SPRITE, angle)


  def get_pix_pos(self):
    return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
    (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

  def time_to_move(self):
      #Eixo X
      if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
          if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
              return True
      #Eixo Y
      if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
          if self.direction == vec(0, 1) or self.direction == vec(0, -1):
              return True

  def can_move(self):
      for wall in self.app.walls:
          if vec(self.grid_pos+self.direction) == wall:
              return False
      return True