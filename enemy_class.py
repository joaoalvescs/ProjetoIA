import pygame
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.number = number
        self.direction = vec(1, 0)
        self.personality = self.set_personality()
        #print(self.personality)


        self.angle = -90
        self.last_direction = 'right'
        self.POLICE_SPRITE = pygame.image.load('./sprites/police.png').convert_alpha()
        self.POLICE_SPRITE = pygame.transform.scale(self.POLICE_SPRITE, (self.app.cell_width, self.app.cell_height))
        self.POLICE_SPRITE = pygame.transform.rotate(self.POLICE_SPRITE, self.angle)


    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move:
            self.move()
        pass

    def draw(self, app):
        self.app = app

        # Inserindo inimigo na tela
        app.screen.blit(self.POLICE_SPRITE, (int(self.pix_pos.x - 10), int(self.pix_pos.y - 10)))


    def time_to_move(self):
        pass

    def move(self):
        pass

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)


    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"