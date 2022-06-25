import random
import sys
import time

import pygame

button_gap_size = 20
button_size = 250
flash_delay = 200
flash_speed = 500
fps = 30
timeout = 4
window_height = 600
window_width = 760

black = (0, 0, 0)
blue = (0, 0, 155)
bright_blue = (0, 0, 255)
bright_green = (0, 255, 0)
bright_red = (255, 0, 0)
bright_yellow = (255, 255, 0)
dark_gray = (40, 40, 40)
green = (0, 155, 0)
red = (155, 0, 0)
yellow = (155, 155, 0)
white = (255, 255, 255)

background_color = black

x_margin = int((window_width - (2 * button_size) - button_gap_size) / 2)
y_margin = int((window_height - (2 * button_size) - button_gap_size) / 2)

yellow_rect = pygame.Rect(x_margin, y_margin, button_size, button_size)
blue_rect = pygame.Rect(x_margin + button_size + button_gap_size, y_margin, button_size, button_size)
red_rect = pygame.Rect(x_margin, y_margin + button_size + button_gap_size, button_size, button_size)
green_rect = pygame.Rect(x_margin + button_size + button_gap_size, y_margin + button_size + button_gap_size,
                         button_size, button_size)


def main():
    global fps_clock, display_surf, basic_font, beep1, beep2, beep3, beep4

    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Simon")

    basic_font = pygame.font.Font("Cousine for Powerline.ttf", 13)

    info_surf = basic_font.render('Match the pattern by clicking on the button or using the Q, W, S, A keys.', 1,
                                  white)
    info_rect = info_surf.get_rect()
    info_rect.topleft = (10, window_height - 25)
    beep1 = pygame.mixer.Sound("sounds/beep1.oga")
    beep2 = pygame.mixer.Sound("sounds/beep2.oga")
    beep3 = pygame.mixer.Sound("sounds/beep3.oga")
    beep4 = pygame.mixer.Sound("sounds/beep4.oga")

    pattern = []
    current_step = 0
    last_click_time = 0
    score = 0

    waiting_for_input = False

    while True:
        clicked_button = None

        display_surf.fill(background_color)
        draw_buttons()

        score_surface = basic_font.render('Score: ' + str(score), 1, white)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (window_width - 100, 10)
        display_surf.blit(score_surface, score_rect)

        display_surf.blit(info_surf, info_rect)

        check_for_quit()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                clicked_button = get_button_clicked(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    clicked_button = yellow
                elif event.key == pygame.K_w:
                    clicked_button = blue
                elif event.key == pygame.K_a:
                    clicked_button = red
                elif event.key == pygame.K_s:
                    clicked_button = green

        if not waiting_for_input:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((yellow, blue, red, green)))
            for button in pattern:
                flash_button_animation(button)
                pygame.time.wait(flash_delay)
            waiting_for_input = True
        else:
            if clicked_button and clicked_button == pattern[current_step]:
                flash_button_animation(clicked_button)
                current_step += 1
                last_click_time = time.time()

                if current_step == len(pattern):
                    change_background_animation()
                    score += 1
                    waiting_for_input = False
                    current_step = 0
            elif (clicked_button and clicked_button != pattern[current_step]) or (current_step != 0 and time.time() -
                                                                                timeout > last_click_time):
                game_over_animation()
                pattern = []
                current_step = 0
                waiting_for_input = False
                score = 0
                pygame.time.wait(2000)
                change_background_animation()
        pygame.display.update()
        fps_clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(pygame.QUIT):
        terminate()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flash_button_animation(color, animation_speed=50):
    if color == yellow:
        sound = beep1
        flash_color = bright_yellow
        rectangle = yellow_rect
    elif color == blue:
        sound = beep2
        flash_color = bright_blue
        rectangle = blue_rect
    elif color == red:
        sound = beep3
        flash_color = bright_red
        rectangle = red_rect
    elif color == green:
        sound = beep4
        flash_color = bright_green
        rectangle = green_rect

    original_surf = display_surf.copy()
    flash_surf = pygame.Surface((button_size, button_size))
    flash_surf = flash_surf.convert_alpha()
    r, g, b = flash_color
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animation_speed * step):
            check_for_quit()
            display_surf.blit(original_surf, (0, 0))
            flash_surf.fill((r, g, b, alpha))
            display_surf.blit(flash_surf, rectangle.topleft)
            pygame.display.update()
            fps_clock.tick(fps)

    display_surf.blit(original_surf, (0, 0))


def draw_buttons():
    pygame.draw.rect(display_surf, yellow, yellow_rect)
    pygame.draw.rect(display_surf, blue, blue_rect)
    pygame.draw.rect(display_surf, red, red_rect)
    pygame.draw.rect(display_surf, green, green_rect)


def change_background_animation(animation_speed=40):
    global background_color
    new_background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    new_background_surf = pygame.Surface((window_width, window_height))
    new_background_surf = new_background_surf.convert_alpha()
    r, g, b = new_background_color
    for alpha in range(0, 255, animation_speed):
        check_for_quit()
        display_surf.fill(background_color)

        new_background_surf.fill((r, g, b, alpha))
        display_surf.blit(new_background_surf, (0, 0))

        draw_buttons()

        pygame.display.update()
        fps_clock.tick(fps)
    background_color = new_background_color


def game_over_animation(color=white, animation_speed=50):
    original_surf = display_surf.copy()
    flash_surf = pygame.Surface(display_surf.get_size())
    flash_surf = flash_surf.convert_alpha()
    beep1.play()
    beep2.play()
    beep3.play()
    beep4.play()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animation_speed * step):
                check_for_quit()
                flash_surf.fill((r, g, b, alpha))
                display_surf.blit(original_surf, (0, 0))
                display_surf.blit(flash_surf, (0, 0))
                draw_buttons()
                pygame.display.update()
                fps_clock.tick(fps)


def get_button_clicked(x, y):
    if yellow_rect.collidepoint((x, y)):
        return yellow
    elif blue_rect.collidepoint((x, y)):
        return blue
    elif red_rect.collidepoint((x, y)):
        return red
    elif green_rect.collidepoint((x, y)):
        return green
    return None


if __name__ == '__main__':
    main()
