import queue
from lib.classes import *
from lib.draw_functions import draw, init_cells, reset_cells

pygame.init()

pygame.display.set_caption("Pathfinding Visualiser")

# Set the FPS to 60
FPS = 60
clock = pygame.time.Clock()

def a_star(cells, start_cell, end_cell):
    """Implements the A* algorithm using Manhattan distance as the heuristic"""
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
            return parent

        x, y = current_cell.get_coords()
        for i in range(4):
            next_cell = cells[x + coords_x[i]][y + coords_y[i]]
            temp_g_val = g_val[current_cell] + 1

            if temp_g_val < g_val[next_cell]:
                g_val[next_cell] = temp_g_val
                f_val[next_cell] = temp_g_val + next_cell.get_heuristic_value(end_cell)
                parent[next_cell] = current_cell
                if next_cell.is_available():
                    count += 1
                    pq.put((f_val[next_cell], count, next_cell))
                    if next_cell != end_cell:
                        next_cell.make_neighbour()

        draw(cells)

        if current_cell != start_cell:
            current_cell.make_visited()
    return None

def draw_best_path(cells, start_cell, end_cell, parent):
    """Draws the best path to reach the end cell from the start cell"""
    if parent == None:
        return
    while parent[end_cell] != start_cell:
        end_cell = parent[end_cell]
        end_cell.make_path()
        draw(cells)

def listen_for_events(cells, start_cell, end_cell):
    """Event listener"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return (False, start_cell, end_cell)
        if pygame.mouse.get_pressed()[0]:
            if not start_cell:
                for row in cells:
                    for cell in row:
                        if (cell.rectangle.collidepoint(pygame.mouse.get_pos())) \
                                and not cell.is_border():
                            cell.make_start()
                            start_cell = cell
                            break
            elif not end_cell:
                for row in cells:
                    for cell in row:
                        if cell.rectangle.collidepoint(pygame.mouse.get_pos()) \
                                and not cell.is_start() and not cell.is_border():
                            cell.make_end()
                            end_cell = cell
                            break
            else:
                for row in cells:
                    for cell in row:
                        if not cell.is_start() and not cell.is_end() and not cell.is_border() \
                                and cell.rectangle.collidepoint(pygame.mouse.get_pos()):
                            cell.make_obstacle()
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
                draw_best_path(cells, start_cell, end_cell, a_star(cells, start_cell, end_cell))
            elif event.key == pygame.K_r:
                start_cell = None 
                end_cell = None 
                reset_cells(cells)
    return (True, start_cell, end_cell)

def main():
    cells = init_cells()
    running = True
    start_cell, end_cell = None, None
    while running:
        clock.tick(FPS)
        draw(cells)
        running, start_cell, end_cell = listen_for_events(cells, start_cell, end_cell)

main()

pygame.quit()
