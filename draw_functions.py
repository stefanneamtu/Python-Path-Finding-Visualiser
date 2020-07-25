from classes import *

# Initialise the screen 
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Variables
GRID_WIDTH = WIDTH // 20
GRID_HEIGHT = HEIGHT // 20

CELL_SIZE = 20
CELL_COUNT = WIDTH * HEIGHT // (CELL_SIZE ** 2) 

def create_border(cells):
    """Creates the border of the grid"""
    for x in range(GRID_WIDTH):
        cells[x][0].make_border()
        cells[x][GRID_HEIGHT - 1].make_border()
    for x in range(GRID_HEIGHT):
        cells[0][x].make_border()
        cells[GRID_WIDTH - 1][x].make_border()

def init_cells():
    """Creates the cells"""
    cells = []
    for x in range(GRID_WIDTH):
        cells.append([])
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cells[x].append(Cell(rect, Colours.WHITE, x, y))
    create_border(cells)
    return cells

def draw_cells(cells):
    """Draws all the rectangles on the screen"""
    for row in cells:
        for cell in row:
            cell.draw_cell(SCREEN)

def draw_grid():
    """Draws the lines"""
    for x in range(GRID_HEIGHT):
        pygame.draw.line(SCREEN, Colours.BLACK, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE))
        for y in range(GRID_WIDTH):
            pygame.draw.line(SCREEN, Colours.BLACK, (y * CELL_SIZE, 0), (y * CELL_SIZE, HEIGHT))

def reset_cells(cells):
    """Resets all cells"""
    for row in cells:
        for cell in row:
            cell.reset_cell()
    create_border(cells)

def draw(cells):
    """Draw everything"""
    draw_cells(cells)
    draw_grid()
    pygame.display.update()

