from snake import Snake
from fruit import Fruit
from pygame.math import Vector2
import pygame
import sys


class Game():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    cell_size = 40
    cell_number = 18
    screen = pygame.display.set_mode(
        (cell_number * cell_size, cell_number * cell_size))
    apple = pygame.image.load(
        '../resources/graphics/apple.png').convert_alpha()
    game_font = pygame.font.Font(
        '../resources/font/PoetsenOne-Regular.ttf', 25)
    clock = pygame.time.Clock()
    snake = Snake(cell_size, screen)
    fruit = Fruit(cell_number, cell_size, screen, apple)

    SCREEN_UPDATE = pygame.USEREVENT
    snake_velocity = 180
    pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        global snake_velocity, SCREEN_UPDATE
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            snake_velocity = snake_velocity - 3
            pygame.time.set_timer(self.SCREEN_UPDATE, snake_velocity)

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not -1 < self.snake.body[0].x < self.cell_number or not -1 < self.snake.body[0].y < self.cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_f:
                    return

    def game_over(self):
        global snake_velocity
        self.snake.reset()
        snake_velocity = 180
        pygame.time.set_timer(self.SCREEN_UPDATE, snake_velocity)

    def draw_grass(self):
        global screen
        grass_color = (167, 209, 61)
        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(self.cell_size * self.cell_number - 60)
        score_y = int(self.cell_size * self.cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.apple, apple_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)

