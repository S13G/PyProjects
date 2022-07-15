import random
import sys

import pygame

board_height = 4
board_width = 4
tile_size = 80
window_height = 530
window_width = 670
fps = 30
blank = None

black = (0, 0, 0)
fade_orange = (240, 180, 85)
dark_turquoise = (3, 54, 73)
light_orange = (200, 155, 23)
white = (0, 0, 0)

basic_font_size = 18
bg_color = dark_turquoise
border_color = fade_orange
text_color = white
tile_color = light_orange

button_color = white
button_text_color = black
message_color = white

x_margin = int((window_width - (tile_size * board_width + (board_width - 1))) / 2)
y_margin = int((window_height - (tile_size * board_height + (board_height - 1))) / 2)

down = 'down'
left = 'left'
right = 'right'
up = 'up'


def main():
    global fps_clock, display_surf, basic_font, reset_surf, reset_rect, new_surf, new_rect, solve_surf, solve_rect

    pygame.init()

    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption('Puzzle Slide')

    basic_font = pygame.font.Font("Source Code Pro for Powerline.otf", basic_font_size)

    reset_surf, reset_rect = make_text('Reset Game', text_color, tile_color, window_width - 120, window_height - 90)

    new_surf, new_rect = make_text('New Game', text_color, tile_color, window_width - 120, window_height - 60)

    solve_surf, solve_rect = make_text('Solve Game', text_color, tile_color, window_width - 120, window_height - 30)

    main_board, solution_sequence = generate_new_puzzle(80)
    solved_board = get_starting_board()

    all_moves = []

    while True:
        slide_to = None
        message = ''
        if main_board == solved_board:
            message = "Solved!"

        draw_board(main_board, message)

        check_for_quit()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                spot_x, spot_y = get_spot_clicked(main_board, event.pos[0], event.pos[1])
                if (spot_x, spot_y) == (None, None):
                    if reset_rect.collidepoint(event.pos):
                        reset_animation(main_board, all_moves)

                        all_moves = []
                    elif new_rect.collidepoint(event.pos):
                        main_board, solution_sequence = generate_new_puzzle(80)

                        all_moves = []
                    elif solve_rect.collidepoint(event.pos):
                        reset_animation(main_board, solution_sequence + all_moves)

                        all_moves = []
                else:
                    blank_x, blank_y = get_blank_position(main_board)
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        slide_to = left
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        slide_to = right
                    elif spot_x == blank_x + spot_y == blank_y + 1:
                        slide_to = up
                    elif spot_x == blank_x + spot_y == blank_y - 1:
                        slide_to = down
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a) and is_valid_move(main_board, left):
                    slide_to = left
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and is_valid_move(main_board, right):
                    slide_to = right
                elif event.key in (pygame.K_UP, pygame.K_w) and is_valid_move(main_board, up):
                    slide_to = up
                elif event.key in (pygame.K_DOWN, pygame.K_s) and is_valid_move(main_board, down):
                    slide_to = down

        if slide_to:
            slide_animation(main_board, slide_to, 'Click tile or press arrow keys to slide.', 8)
            make_move(main_board, slide_to)
            all_moves.append(slide_to)

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


def get_starting_board():
    counter = 1
    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(counter)
            counter += board_width
        board.append(column)
        counter -= board_width * (board_height - 1) + board_width - 1

    board[board_width - 1][board_height - 1] = None
    return board


def get_blank_position(board):
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] is None:
                return x, y


def make_move(board, move):
    blank_x, blank_y = get_blank_position(board)

    if move == up:
        board[blank_x][blank_y], board[blank_x][blank_y + 1] = board[blank_x][blank_y + 1], board[blank_x][blank_y]
    elif move == down:
        board[blank_x][blank_y], board[blank_x][blank_y - 1] = board[blank_x][blank_y - 1], board[blank_x][blank_y]
    elif move == left:
        board[blank_x][blank_y], board[blank_x + 1][blank_y] = board[blank_x + 1][blank_y], board[blank_x][blank_y]
    elif move == right:
        board[blank_x][blank_y], board[blank_x - 1][blank_y] = board[blank_x - 1][blank_y], board[blank_x][blank_y]


def is_valid_move(board, move):
    blank_x, blank_y = get_blank_position(board)
    return (move == up and blank_y != len(board[0]) - 1) or (move == down and blank_y != 0) or \
           (move == left and blank_x != len(board) - 1) or (move == right and blank_x != 0)


def get_random_move(board, last_move=None):
    valid_moves = [up, down, left, right]

    if last_move == up or not is_valid_move(board, down):
        valid_moves.remove(down)
    if last_move == down or not is_valid_move(board, up):
        valid_moves.remove(up)
    if last_move == left or not is_valid_move(board, right):
        valid_moves.remove(right)
    if last_move == right or not is_valid_move(board, left):
        valid_moves.remove(left)

    return random.choice(valid_moves)


def get_left_top_of_tile(tile_x, tile_y):
    LEFT = x_margin + (tile_x * tile_size) + (tile_x - 1)
    top = y_margin + (tile_y * tile_size) + (tile_y - 1)
    return LEFT, top


def get_spot_clicked(board, x, y):
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            LEFT, top = get_left_top_of_tile(tile_x, tile_y)
            tile_rect = pygame.Rect(LEFT, top, tile_size, tile_size)
            if tile_rect.collidepoint(x, y):
                return tile_x, tile_y
    return None, None


def draw_tile(tile_x, tile_y, number, adj_x=0, adj_y=0):
    LEFT, top = get_left_top_of_tile(tile_x, tile_y)
    pygame.draw.rect(display_surf, tile_color, (LEFT + adj_x, top + adj_y, tile_size, tile_size))
    text_surf = basic_font.render(str(number), True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = LEFT + int(tile_size / 2) + adj_x, top + int(tile_size / 2) + adj_y
    display_surf.blit(text_surf, text_rect)


def make_text(text, color, background_color, top, LEFT):
    text_surf = basic_font.render(text, True, color, background_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, LEFT)
    return text_surf, text_rect


def draw_board(board, message):
    display_surf.fill(bg_color)
    if message:
        text_surf, text_rect = make_text(message, message_color, bg_color, 5, 5)
        display_surf.blit(text_surf, text_rect)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                draw_tile(tile_x, tile_y, board[tile_x][tile_y])

    LEFT, top = get_left_top_of_tile(0, 0)
    width = board_width * tile_size
    height = board_height * tile_size

    pygame.draw.rect(display_surf, border_color, (LEFT - 5, top - 5, width + 11, height + 11), 4)

    display_surf.blit(reset_surf, reset_rect)
    display_surf.blit(new_surf, new_rect)
    display_surf.blit(solve_surf, solve_rect)


def slide_animation(board, direction, message, animation_speed):
    blank_x, blank_y = get_blank_position(board)
    if direction == up:
        move_x = blank_x
        move_y = blank_y + 1
    elif direction == down:
        move_x = blank_x
        move_y = blank_y - 1
    elif direction == left:
        move_x = blank_x + 1
        move_y = blank_y
    elif direction == right:
        move_x = blank_x - 1
        move_y = blank_y

    draw_board(board, message)
    base_surf = display_surf.copy()

    move_left, move_top = get_left_top_of_tile(move_x, move_y)
    pygame.draw.rect(base_surf, bg_color, (move_left, move_top, tile_size, tile_size))

    for i in range(0, tile_size, animation_speed):
        check_for_quit()
        display_surf.blit(base_surf, (0, 0))
        if direction == up:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, -i)
        if direction == down:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, i)
        if direction == left:
            draw_tile(move_x, move_y, board[move_x][move_y], -i, 0)
        if direction == right:
            draw_tile(move_x, move_y, board[move_x][move_y], i, 0)

        pygame.display.update()
        fps_clock.tick(fps)


def generate_new_puzzle(num_slides):
    sequence = []
    board = get_starting_board()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None
    for i in range(num_slides):
        move = get_random_move(board, last_move)
        slide_animation(board, move, 'Generating new puzzle...', int(tile_size / 3))
        make_move(board, move)
        sequence.append(move)
        last_move = move
    return board, sequence


def reset_animation(board, all_moves):
    rev_all_moves = all_moves[:]
    rev_all_moves.reverse()

    for move in rev_all_moves:
        if move == up:
            opposite_move = down
        elif move == down:
            opposite_move = up
        elif move == right:
            opposite_move = left
        elif move == left:
            opposite_move = right
        slide_animation(board, opposite_move, '', int(tile_size / 2))
        make_move(board, opposite_move)


if __name__ == '__main__':
    main()
