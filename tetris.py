import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

ver = '1.0'
# SHAPE FORMATS

S = [['.....',
    '.....',
    '..00.',
    '.00..',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface, scale_factor):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    scaled_label = pygame.transform.scale(label, (int(label.get_width() * scale_factor), 
                                                   int(label.get_height() * scale_factor)))   
    surface.blit(scaled_label, (top_left_x + play_width / 2 - (scaled_label.get_width() / 2),
                                top_left_y + play_height / 2 - scaled_label.get_height() / 2))

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc 

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 80
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, score, level, grid):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Draw the score
    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(score_label, (top_left_x + play_width + 20, top_left_y + 100))
    
    # Draw the level
    level_label = font.render(f'Level: {level}', 1, (255, 255, 255))
    surface.blit(level_label, (top_left_x + play_width + 20, top_left_y + 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # Draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    # Draw version
    version_label = font.render('ver ' + ver, 1, (255, 255, 255))
    surface.blit(version_label, (s_width - version_label.get_width() - 10, s_height - version_label.get_height() - 10))


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)  # Khởi tạo grid ngay tại đây

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.3
    score = 0
    level = 1
    
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if score > 500 :
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005
                level += 1
        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            # Tăng tốc khi ấn giữ nút S hoặc DOWN
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            cleared_rows = clear_rows(grid, locked_positions)
            if cleared_rows > 0:
                score += cleared_rows * 100

        draw_window(win, score, level, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255,255,255), win, 1)
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    scale_factor = 1  
    scale_speed = 0.0002
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press A key to begin.', 60, (255, 255, 255), win, scale_factor)
        scale_factor += scale_speed
        if scale_factor > 1.05 or scale_factor < 0.9:
            scale_speed = -scale_speed
        pygame.display.update()
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    main()
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()
