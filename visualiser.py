import pygame
from cell_class import *

pygame.init()

# Initialise the screen 
WIDTH, HEIGHT = 1000, 600
CELL_SIZE = 20
CELL_COUNT = WIDTH * HEIGHT // (CELL_SIZE ** 2) 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pathfinding Visualiser")

# Variables
cells = []
GRID_WIDTH = WIDTH // 20
GRID_HEIGHT = HEIGHT // 20

# Set the FPS to 60
FPS = 60
clock = pygame.time.Clock()

def init_cells():
    ind = 0
    for x in range(GRID_WIDTH):
        cells.append([])
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cells[x].append(Cell(rect, Colours.WHITE, x, y))
            ind += 1
    for x in range(GRID_WIDTH):
        cells[x][0].change_colour(Colours.GREY) 
        cells[x][GRID_HEIGHT - 1].change_colour(Colours.GREY)
    for x in range(GRID_HEIGHT):
        cells[0][x].change_colour(Colours.GREY)
        cells[GRID_WIDTH- 1][x].change_colour(Colours.GREY)

def draw_cells():
    for row in cells:
        for cell in row:
            cell.draw_cell(SCREEN)

def draw_grid():
    for x in range(GRID_HEIGHT):
        pygame.draw.line(SCREEN, Colours.BLACK, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE))
        for y in range(GRID_WIDTH):
            pygame.draw.line(SCREEN, Colours.BLACK, (y * CELL_SIZE, 0), (y * CELL_SIZE, HEIGHT))

def draw():
    draw_cells()
    draw_grid()
    pygame.display.update()

# Temporary path finding function
def path_find(start_cell, end_cell, cells):
    x, y = start_cell.get_coords()
    if not start_cell.is_border() and not start_cell.is_visited() and not start_cell == end_cell and not start_cell.is_obstacle():
        if not start_cell.is_start():
            start_cell.change_colour(Colours.GREEN)
        draw()
        path_find(cells[x + 1][y], end_cell, cells)
        path_find(cells[x - 1][y], end_cell, cells)
        path_find(cells[x][y - 1], end_cell, cells)
        path_find(cells[x][y + 1], end_cell, cells)

def listen_for_events(start_cell, end_cell):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
          (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return (False, start_cell, end_cell)
        if pygame.mouse.get_pressed()[0]:
            if not start_cell:
                for row in cells:
                    for cell in row:
                        if (cell.rectangle.collidepoint(pygame.mouse.get_pos())) and not cell.is_border():
                            cell.change_colour(Colours.ORANGE)
                            start_cell = cell
                            break
            elif not end_cell:
                for row in cells:
                    for cell in row:
                        if cell.rectangle.collidepoint(pygame.mouse.get_pos()) \
                          and not cell.is_start() and not cell.is_border():
                            cell.change_colour(Colours.CYAN)
                            end_cell = cell
                            break
            else:
                for row in cells:
                    for cell in row:
                        if not cell.is_start() and not cell.is_end() and not cell.is_border() \
                          and cell.rectangle.collidepoint(pygame.mouse.get_pos()):
                            cell.change_colour(Colours.BLACK)
        if pygame.mouse.get_pressed()[2]:
            for row in cells:
                for cell in row:
                    if cell.rectangle.collidepoint(pygame.mouse.get_pos()):
                        if cell.is_start():
                            start_cell = None 
                        elif cell.is_end():
                            end_cell = None 
                        cell.reset_cell()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                path_find(start_cell, end_cell, cells)
    return (True, start_cell, end_cell)

def main():
    init_cells()
    running = True
    start_cell, end_cell = None, None
    while running:
        clock.tick(FPS)
        draw()
        running, start_cell, end_cell = listen_for_events(start_cell, end_cell)

main()

pygame.quit()
