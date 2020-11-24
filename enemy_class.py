
import random
from settings import *
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.direction = vec(1, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()
        # self.colour = self.set_colour()
        # print(self.personality)

        self.angle = -90
        self.last_direction = 'right'
        self.POLICE_SPRITE = pygame.image.load('./sprites/police.png').convert_alpha()
        self.POLICE_SPRITE = pygame.transform.scale(
            self.POLICE_SPRITE, (self.app.cell_width, self.app.cell_height))
        self.POLICE_SPRITE = pygame.transform.rotate(
            self.POLICE_SPRITE, self.angle)

    def update(self):
        if self.target != self.grid_pos:
            self.target = self.set_target()
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

    def draw(self, app):
        self.app = app

        # Inserindo inimigo na tela
        app.screen.blit(self.POLICE_SPRITE, (int(
            self.pix_pos.x - 10), int(self.pix_pos.y - 10)))

    def set_speed(self):
        if self.personality in ["speedy","scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1,1)
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2,1)
            else:
                return vec(COLS-2, ROWS-2)

    def time_to_move(self):
      # Eixo X
      if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
          if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
              return True
      # Eixo Y
      if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
          if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
              return True
      return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy": 
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def rotate_enemy(self, come_direction):
        angle = 0
        # IR P/ ESQUERDA
        if come_direction == vec(-1,0):
            if self.last_direction == 'right':
                angle = -180
            if self.last_direction == 'down':
                angle = -90
            if self.last_direction == 'up':
                angle = 90

            self.POLICE_SPRITE = pygame.transform.rotate(self.POLICE_SPRITE, angle)
            self.last_direction = 'left'

        # IR P/ DIREITA
        if come_direction == vec(1,0):
            if self.last_direction == 'left':
                angle = 180
            if self.last_direction == 'down':
                angle = 90
            if self.last_direction == 'up':
                angle = -90

            self.POLICE_SPRITE = pygame.transform.rotate(self.POLICE_SPRITE, angle)
            self.last_direction = 'right'

        # IR P/ CIMA
        if come_direction == vec(0,-1):
            if self.last_direction == 'left':
                angle = -90
            if self.last_direction == 'right':
                angle = 90
            if self.last_direction == 'down':
                angle = 180

            self.POLICE_SPRITE = pygame.transform.rotate(self.POLICE_SPRITE, angle)
            self.last_direction = 'up'

        # IR P/ BAIXO
        if come_direction == vec(0,1):
            if self.last_direction == 'left':
                angle = 90
            if self.last_direction == 'right':
                angle = -90
            if self.last_direction == 'up':
                angle = 180

            self.POLICE_SPRITE = pygame.transform.rotate(self.POLICE_SPRITE, angle)
            self.last_direction = 'down'

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        self.rotate_enemy(vec(xdir, ydir))

        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.STAR_ALGORITMO([int(self.grid_pos.x), int(self.grid_pos.y)], [
                         int(target[0]), int(target[1])])
        return path[1]

    def STAR_ALGORITMO(self, start, target):
        grid = [[1 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 0
        
        # print(grid)
        matrix = Grid(matrix=grid)
        # print('start:' + str(start))
        start = matrix.node(start[0], start[1])
        target = matrix.node(target[0], target[1])
        finder = AStarFinder()
        path, runs = finder.find_path(start, target, matrix)

        return path

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

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
