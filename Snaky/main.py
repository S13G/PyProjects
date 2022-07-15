import random
import sys

import pygame
from pygame.locals import *

cell_size = 20
fps = 15
window_height = 480
window_width = 640

assert window_height % cell_size == 0, "Window height must be a multiple of cell size."
assert window_width % cell_size == 0, "Window width must be a multiple of cell size."

cell_height = int(window_height / cell_size)
cell_width = int(window_width / cell_size)

black = (0, 0, 0)
dark_gray = (40, 40, 40)
dark_green = (0, 155, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

background_color = black

down = 'down'
left = 'left'
right = 'right'
up = 'up'

head = 0


def main():
    global fps_clock, display_surface, basic_font

    pygame.init()
    basic_font = pygame.font.Font('Ubuntu Mono derivative Powerline.ttf', 16)
    display_surface = pygame.display.set_mode(window_width, window_height)
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Snaky')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def run_game():
    start_x = random.randint(5, cell_width - 6)
    start_y = random.randint(5, cell_height - 6)

    snaky_coordinates = [{'x': start_x, 'y': start_y},
                         {'x': start_x - 1, 'y': start_y},
                         {'x': start_x - 2, 'y': start_y}]

    direction = right

    fruit = get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != right:
                    direction = left
                elif (event.key == K_RIGHT or event.key == K_d) and direction != left:
                    direction = right
                elif (event.key == K_UP or event.key == K_w) and direction != down:
                    direction = up
                elif (event.key == K_DOWN or event.key == K_s) and direction != up:
                    direction = down
                elif event.key == K_ESCAPE:
                    terminate()

        if snaky_coordinates[head]['x'] == -1 or snaky_coordinates[head]['x'] == cell_width or \
                snaky_coordinates[head]['y'] == -1 or snaky_coordinates[head]['y'] == cell_height:
            return

        for snaky_body in snaky_coordinates[1:]:
            if snaky_body['x'] == snaky_coordinates[head]['x'] and snaky_body['y'] == snaky_coordinates[head]['y']:
                return

        if snaky_coordinates[head]['x'] == fruit['x'] and snaky_coordinates[head]['y'] == fruit['y']:
            apple = get_random_location()
        else:
            del snaky_coordinates[-1]

        if direction == up:
            new_head = {'x': snaky_coordinates[head]['x'], 'y': snaky_coordinates[head]['y'] - 1}
        elif direction == down:
            new_head = {'x': snaky_coordinates[head]['x'], 'y': snaky_coordinates[head]['y'] + 1}
        elif direction == left:
            new_head = {'x': snaky_coordinates[head]['x'] - 1, 'y': snaky_coordinates[head]['y']}
        elif direction == right:
            new_head = {'x': snaky_coordinates[head]['x'] + 1, 'y': snaky_coordinates[head]['y']}

        snaky_coordinates.insert(0, new_head)
        display_surface.fill(background_color)
        draw_fruit(fruit)
        draw_grid()
        draw_score(len(snaky_coordinates) - 3)
        draw_snake(snaky_coordinates)
        pygame.display.update()
        fps_clock.tick(fps)


def message_key():
    key_surface = basic_font.render('Press a key to play.', True, dark_gray)
    key_rect = key_surface.get_rect()
    key_rect.topleft = (window_width - 200, window_height - 200)
    display_surface.blit(key_surface, key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen():
    title_font = pygame.font.Font('Ubuntu Mono derivative Powerline.ttf', 100)
    first_title_surface = title_font.render('Snaky!', True, white, dark_green)
    second_title_surface = title_font.render('Let\'s go!', True, green)

    degrees1 = 0
    degrees2 = 0

    while True:
        display_surface(background_color)
        first_rotated_surface = pygame.transform.rotate(first_title_surface, degrees1)
        first_rotated_rect = first_rotated_surface.get_rect()
        first_rotated_rect.center = (window_width / 2, window_height / 2)
        display_surface.blit(first_rotated_surface, first_rotated_rect)

        second_rotated_surface = pygame.transform.rotate(second_title_surface, degrees2)
        second_rotated_rect = second_rotated_surface.get_rect()
        second_rotated_rect.center = (window_width / 2, window_height / 2)
        display_surface.blit(second_rotated_surface, second_rotated_rect)

        message_key()

        if check_for_key_press():
            pygame.event.get()
            return
        pygame.display.update()
        fps_clock.tick(fps)
        degrees1 += 3
        degrees2 += 7


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, cell_width - 1), 'y': random.randint(0, cell_height - 1)}


def show_game_over_screen():
    game_over_font = pygame.font.Font('Ubuntu Mono derivative Powerline.ttf', 150)
    game_surface = game_over_font.render('Game', True, white)
    over_surface = game_over_font.render('Over', True, white)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (window_width / 2, 10)
    over_rect.midtop = (window_width / 2, game_rect.height + 10 + 25)

    display_surface.blit(game_surface, game_rect)
    display_surface.blit(over_surface, over_rect)

    message_key()
    pygame.display.update()
    pygame.time.wait(100)
    check_for_key_press()

    while True:
        if check_for_key_press():
            pygame.event.get()
            return


def draw_score(score):
    score_surface = basic_font.render('Score: %s' % score, True, white)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (window_width - 120, 10)
    display_surface.blit(score_surface, score_rect)


def draw_snake(snaky_coordinates):
    for coordinate in snaky_coordinates:
        x = coordinate['x'] * cell_size
        y = coordinate['y'] * cell_size

        snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(display_surface, dark_green, snake_segment_rect)