from snake import SNAKE
from fruit import FRUIT
from pygame.math import Vector2
import pygame
import sys


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 18
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load(
    '../resources/graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(
    '../resources/font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
snake_velocity = 180
pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)
snake = SNAKE(cell_size, screen)
fruit = FRUIT(cell_number, cell_size, screen, apple)


def update():
    snake.move_snake()
    check_collision()
    check_fail()


def draw_elements():
    draw_grass()
    fruit.draw_fruit()
    snake.draw_snake()
    draw_score()


def check_collision():
    if fruit.pos == snake.body[0]:
        global snake_velocity
        fruit.randomize()
        snake.add_block()
        snake.play_crunch_sound()
        snake_velocity = snake_velocity - 3
        pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)

    for block in snake.body[1:]:
        if block == fruit.pos:
            fruit.randomize()


def check_fail():
    if not -1 < snake.body[0].x < cell_number or not -1 < snake.body[0].y < cell_number:
        game_over()

    for block in snake.body[1:]:
        if block == snake.body[0]:
            game_over()


def game_over():
	global snake_velocity
	snake.reset()
	snake_velocity = 180
	pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)


def draw_grass():
    grass_color = (167, 209, 61)
    for row in range(cell_number):
        if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)


def draw_score():
    score_text = str(len(snake.body) - 3)
    score_surface = game_font.render(score_text, True, (56, 74, 12))
    score_x = int(cell_size * cell_number - 60)
    score_y = int(cell_size * cell_number - 40)
    score_rect = score_surface.get_rect(center=(score_x, score_y))
    apple_rect = apple.get_rect(
        midright=(score_rect.left, score_rect.centery))
    bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                          apple_rect.width + score_rect.width + 6, apple_rect.height)

    pygame.draw.rect(screen, (167, 209, 61), bg_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(apple, apple_rect)
    pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


# main_game = MAIN(snake, fruit)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction.y != 1:
                    snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if snake.direction.x != -1:
                    snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if snake.direction.y != -1:
                    snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if snake.direction.x != 1:
                    snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    draw_elements()
    pygame.display.update()
    clock.tick(200)
