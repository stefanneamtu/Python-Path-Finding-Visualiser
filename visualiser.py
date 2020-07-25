import pygame
import queue
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
    for x in range(GRID_WIDTH):
        cells.append([])
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cells[x].append(Cell(rect, Colours.WHITE, x, y))
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

def bfs(start_cell, end_cell):
    q = queue.SimpleQueue()
    
    coords_x = [1, -1, 0, 0]
    coords_y = [0, 0, 1, -1]

    q.put(start_cell)
    
    found = False
    while not q.empty() and not found:
        cell = q.get()
        if not cell == start_cell:
            cell.change_colour(Colours.GREEN)
        x, y = cell.get_coords()
        for i in range(4):
            next_cell = cells[x + coords_x[i]][y + coords_y[i]]
            if next_cell == end_cell:
                found = True
                break;
            if not next_cell.is_border() and not next_cell == end_cell and \
              not next_cell.is_obstacle() and not next_cell.is_start() and \
              not next_cell.is_visited():
                next_cell.change_colour(Colours.RED)
                draw()
                q.put(next_cell)

def a_star(start_cell, end_cell):
    count = 0
    pq = queue.PriorityQueue()
    pq.put((0, count, start_cell))


    parent = {}

    g_val = {}
    f_val = {}

    for row in cells:
        for cell in row:
            g_val[cell] = float('inf')
            f_val[cell] = float('inf')
    g_val[start_cell] = 0
    f_val[start_cell] = start_cell.get_heuristic_value(end_cell)

    coords_x = [1, -1, 0, 0]
    coords_y = [0, 0, 1, -1]

    while not pq.empty():
        current_cell = pq.get()[2]

        if current_cell == end_cell:
            return True

        x, y = current_cell.get_coords()
        for i in range(4):
            next_cell = cells[x + coords_x[i]][y + coords_y[i]]
            temp_g_val = g_val[current_cell] + 1

            if temp_g_val < g_val[next_cell]:
                g_val[next_cell] = temp_g_val
                f_val[next_cell] = temp_g_val + next_cell.get_heuristic_value(end_cell)
                parent[next_cell] = current_cell
                if not next_cell.is_visited() and not next_cell.is_obstacle() \
                  and not next_cell.is_border():
                    count += 1
                    pq.put((f_val[next_cell], count, next_cell))
                    if next_cell != end_cell:
                        next_cell.change_colour(Colours.RED)

        draw()

        if current_cell != start_cell:
            current_cell.change_colour(Colours.GREEN)


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
                    if cell.rectangle.collidepoint(pygame.mouse.get_pos()) \
                      and not cell.is_border():
                        if cell.is_start():
                            start_cell = None 
                        elif cell.is_end():
                            end_cell = None 
                        cell.reset_cell()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                a_star(start_cell, end_cell)
                #bfs(start_cell, end_cell)
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
