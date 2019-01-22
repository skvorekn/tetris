import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 650
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
'......',
'..00..',
'.00...',
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
# index 0 - 6 represent shape

# data structure for game
# represents different pieces, will be called a bunch of times
# will hold x, y for the piece
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 # add 1 to get the shape we will actually show, from the shape list

def create_grid(locked_pos = {}):
    # create one list for every row in our grid
    # 20 sublists containing 10 colors (10 squares in each row, 20 rows)
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    # locked position if there are already blocks placed in our grid
    # check if any of the positions in locked pos
    # each position in locked_pos will be a color
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    # put shapes in form computer can read, with positions in grid of where blocks exist
    positions = []
    # gives us sublist to get specific shape in list
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        # loop through the line and look for 0 or period
        for j, column in enumerate(row):
            if column == '0':
                # add that position into our list
                positions.append((shape.x + j, shape.y + i))

    # offset positions
    for i, pos in enumerate(positions):
        # move everything to the left and up, so it's more accurate to the screen
        # otherwise will run into errors
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    # check grid to see if we're moving into valid space
    # every possible position in a 10 X 20 grid
    # only add into accepted positions if it's blank
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] # [[(0,1)], [(2,3)]]
    accepted_pos = [j for sub in accepted_pos for j in sub] # [(0,1),(2,3)]

    # convert shape into positions
    formatted = convert_shape_format(shape) #[(),()]

    for pos in formatted:
        if pos not in accepted_pos:
            # if y value is greater than -1
            # only asking if in a valid position if it is not falling from off the grid
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    # check if any of the positions are above the screen
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    # starts above the screen in the middle
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, row, col):
    # draw lines for the grid
    sx = top_left_x
    sy = top_left_y

    # loop through rows
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy+ i*block_size), (sx+ play_width, sy+ i*block_size))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx+ j*block_size, sy),
                             (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    # loop through grid backwards
    for i in range(len(grid)-1, -1, -1):
        # every row in grid
        row = grid[i]
        # if there are no black squares in the row, it is completely filled with shapes
        if (0,0,0) not in row:
            inc += 1
            ind = i
            # get every position in that row
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    # shift every row if we've removed at least one row
    # and add another row at the top so grid stays the same size
    if inc > 0:
        # sort it based on the y value
        # look backwards so we don't overwrite existing rows
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            # if y value is above current index of row we removed
            # don't move anything below the row that is being cleared
            if y < ind:
                # shift every position in the row down
                # inc is the number of rows that we need to shift it down
                newKey = (x, y + inc)
                # newkey with same color value equal to the new position
                locked[newKey] = locked.pop(key)

    # return number of rows cleared
    return inc


def draw_next_shape(shape, surface):
    # show next shape off the screen
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50 # move right
    sy = top_left_y + play_height/2 - 100 # move higher
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score = 0, last_score = 0):
    # black
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans',60)
    label = font.render('Tetris', 1, (255,255,255))

    # middle of the screen
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    # draw the grid objects on the screen
    # loop through every color in our grid and draw it on
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    # 4 = border size
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    # pygame.display.update()

def update_score(nscore):
    score = max_score()

    with open('scores.txt','w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def main(win):

    global grid

    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # how long it takes before each piece starts falling
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        # track how long since the last loop ran
        # raw time gets amount of time since last clock.tick()
        # so how long it took the while loop to run
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # every 5 seconds, increase the speed
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                # 0.01 is very fast
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # check which key is hit
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    # check if it's a valid position
                    if not(valid_space(current_piece, grid)):
                        # move it back if we are going off the screen
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            # shouldn't draw if off the screen
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            # update locked positions
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                # dictionary with locked position: color
                # get each of the positions and update the color of the grid
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("You lost! :(", 80, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press any key to play!', 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game