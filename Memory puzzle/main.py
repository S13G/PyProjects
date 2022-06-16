import random
import sys

import pygame.time

board_width = 10
board_height = 7
box_size = 40
FPS = 30
gap_size = 10
reveal_speed = 8
window_height = 480
window_width = 640

assert (board_width * board_height) % 2 == 0, "Board needs to have an even number of boxes for pairs of matches."

x_margin = int((window_width - (board_width * (box_size + gap_size))) / 2)
y_margin = int((window_height - (board_height * (box_size + gap_size))) / 2)

blue = (0, 0, 255)
cyan = (0, 255, 255)
gray = (100, 100, 100)
green = (0, 255, 0)
navy_blue = (60, 60, 100)
orange = (255, 128, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)

bg_color = navy_blue
box_color = white
highlight_color = blue
light_bg_color = gray

diamond = 'diamond'
donut = 'donut'
lines = 'lines'
oval = 'oval'
square = 'square'

all_colors = (blue, cyan, gray, green, orange, red, yellow)
all_shapes = (diamond, donut, lines, oval, square)

assert len(all_colors) * len(all_shapes) * 2 >= board_width * board_height, \
    "Board is too big for the number of shapes or colors defined."


def main():
    global fps_clock, display_surf
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_width, window_height))

    mouse_x = 0
    mouse_y = 0
    pygame.display.set_caption('Memory Puzzle Game')

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None

    display_surf.fill(bg_color)
    start_game_animation(main_board)

    while True:
        mouse_clicked = False

        display_surf.fill(bg_color)
        draw_board(main_board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        box_x, box_y = get_box_at_pixel(mouse_x, mouse_y)

        if box_x is not None and box_y is not None:
            if not revealed_boxes[box_x][box_y]:
                draw_highlight_box(box_x, box_y)
            if not revealed_boxes[box_x][box_y] and mouse_clicked:
                reveal_boxes_animation(main_board, [(box_x, box_y)])
                revealed_boxes[box_x][box_y] = True

                if first_selection is None:
                    first_selection = (box_x, box_y)
                else:
                    icon1_shape, icon1_color = get_shape_and_color(main_board, first_selection[0], first_selection[1])
                    icon2_shape, icon2_color = get_shape_and_color(main_board, box_x, box_y)

                    if icon1_shape != icon2_shape or icon1_color != icon2_color:
                        pygame.time.wait(1000)
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[box_x][box_y] = False
                    elif has_won(revealed_boxes):
                        game_won_animation(main_board)
                        pygame.time.wait(2000)

                        main_board = get_randomized_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        draw_board(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        start_game_animation(main_board)
                    first_selection = None

        pygame.display.update()
        fps_clock.tick(FPS)


def generate_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(board_width):
        revealed_boxes.append([val] * board_height)
    return revealed_boxes


def get_randomized_board():
    icons = []
    for color in all_colors:
        for shape in all_shapes:
            icons.append((shape, color))

    random.shuffle(icons)
    num_icons_used = int(board_width * board_height / 2)
    icons = icons[:num_icons_used] * 2
    random.shuffle(icons)

    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def split_into_groups_of(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def left_top_cords_of_box(box_x, box_y):
    left = box_x * (box_size + gap_size) + x_margin
    top = box_y * (box_size + gap_size) + y_margin
    return left, top


def get_box_at_pixel(x, y):
    for box_x in range(board_width):
        for box_y in range(board_height):
            left, top = left_top_cords_of_box(box_x, box_y)
            box_rect = pygame.Rect(left, top, box_size, box_size)
            if box_rect.collidepoint(x, y):
                return box_x, box_y
        return None, None


def draw_icon(shape, color, box_x, box_y):
    quarter = int(box_size * 0.25)
    half = int(box_size * 0.5)

    left, top = left_top_cords_of_box(box_x, box_y)

    if shape == donut:
        pygame.draw.circle(display_surf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(display_surf, color, (left + half, top + half), quarter - 5)
    elif shape == square:
        pygame.draw.rect(display_surf, color, (left + quarter, top + quarter, box_size - half, box_size - half))
    elif shape == diamond:
        pygame.draw.polygon(display_surf, color, ((left + half, top), (left + box_size - 1, top + half),
                                                  (left + half, top + box_size - 1), (left, top + half)))
    elif shape == lines:
        for i in range(0, box_size, 4):
            pygame.draw.line(display_surf, color, (left, top + i), (left + i, top))
            pygame.draw.line(display_surf, color, (left + i, top + box_size - 1), (left + box_size - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(display_surf, color, (left, top + quarter, box_size, half))


def get_shape_and_color(board, box_x, box_y):
    return board[box_x][box_y][0], board[box_x][box_y][1]


def draw_box_covers(board, boxes, coverage):
    for box in boxes:
        left, top = left_top_cords_of_box(box[0], box[1])
        pygame.draw.rect(display_surf, bg_color, (left, top, box_size, box_size))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])

        if coverage > 0:
            pygame.draw.rect(display_surf, box_color, (left, top, coverage, box_size))
    pygame.display.update()
    fps_clock.tick(FPS)


def reveal_boxes_animation(board, boxes_to_reveal):
    for coverage in range(box_size, (-reveal_speed) - 1, -reveal_speed):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover):
    for coverage in range(0, box_size + reveal_speed, reveal_speed):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed):
    for box_x in range(board_width):
        for box_y in range(board_height):
            left, top = left_top_cords_of_box(box_x, box_y)
            if not revealed[box_x][box_y]:
                pygame.draw.rect(display_surf, box_color, (left, top, box_size, box_size))
            else:
                shape, color = get_shape_and_color(board, box_x, box_y)
                draw_icon(shape, color, box_x, box_y)


def draw_highlight_box(box_x, box_y):
    left, top = left_top_cords_of_box(box_x, box_y)
    pygame.draw.rect(display_surf, highlight_color, (left - 5, top - 5, box_size + 10, box_size + 10), 4)


def start_game_animation(board):
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(board_width):
        for y in range(board_height):
            boxes.append((x, y))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)

    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(board, box_group)
        cover_boxes_animation(board, box_group)


def game_won_animation(board):
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = light_bg_color
    color2 = bg_color

    for i in range(13):
        color1, color2 = color2, color1
        display_surf.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes):
    for i in revealed_boxes:
        if False in i:
            return False
        return True


if __name__ == '__main__':
    main()
