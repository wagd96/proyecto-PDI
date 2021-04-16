import pygame
import random
from pygame.math import Vector2


class Fruit:
    def __init__(self, cell_number, cell_size, screen, apple):
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.screen = screen
        self.apple = apple
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * self.cell_size), int(self.pos.y * self.cell_size), self.cell_size, self.cell_size)
        self.screen.blit(self.apple, fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, self.cell_number - 1)
        self.y = random.randint(0, self.cell_number - 1)
        self.pos = Vector2(self.x, self.y)
