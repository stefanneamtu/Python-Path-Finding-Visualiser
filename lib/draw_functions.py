from .classes import *

pygame.font.init()

# Initialise the screen 
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BUTTON_FONT = pygame.font.SysFont('comicsans', 80)
INSTR_FONT = pygame.font.SysFont('comicsans', 25)

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
    """Draws the grid"""
    draw_cells(cells)
    draw_grid()
    pygame.display.update()

def draw_best_path(cells, start_cell, end_cell, parent):
    """Draws the best path to reach the end cell from the start cell"""
    if parent == None:
        return
    while parent[end_cell] != start_cell:
        end_cell = parent[end_cell]
        end_cell.make_path()
        draw(cells)

def draw_text(string, colour, y_offset):
    """Draws text on the screen"""
    text = BUTTON_FONT.render(string, 1, colour)
    x = (WIDTH - text.get_width()) // 2
    y = (HEIGHT - text.get_height()) // 2 + y_offset
    return SCREEN.blit(text, (x, y))

def draw_instructions(y_start):
    """Draws the instruction text"""
    instr_string = ['Instructions:', 'ESC - exit', 'R - resets grid', 
            'Enter - starts the algorithm', 'Left click - sets cells', 
            'Right click - resets cells']
    y_offset = 30

    for i in range(len(instr_string)):
        instr_text = INSTR_FONT.render(instr_string[i], 1, Colours.BLACK)
        x = (WIDTH - instr_text.get_width()) // 2
        y = (HEIGHT - instr_text.get_height()) // 2 
        SCREEN.blit(instr_text, (x, y_start + y + y_offset * i))


def start_menu(clock, FPS):
    """Starts the algorithm selection menu"""
    button_rect = None
    button_text = 'Start'
    y_offset = 50

    SCREEN.fill(Colours.MENU_COLOUR)

    draw_instructions(120)

    running = True
    while running:
        clock.tick(FPS)
        draw_text('A* pathing visualiser', Colours.BLUE, -180)
        button_rect = draw_text(button_text, Colours.BLACK, y_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            button_rect = draw_text(button_text, Colours.CYAN, y_offset)

        pygame.display.update()
