import pygame
from cell_class import Cell

pygame.init()

# Initialise the screen 
WIDTH, HEIGHT = 900, 560
CELL_SIZE = 20
CELL_COUNT = WIDTH * HEIGHT // (CELL_SIZE ** 2) 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pathfinding Visualiser")

# Variables
cells = []

# Set the FPS to 60
FPS = 60
clock = pygame.time.Clock()

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def init_grid():
    CELL_SIZE = 20
    ind = 0
    for x in range(WIDTH // 20):
        for y in range(HEIGHT // 20):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cells.append(Cell(rect, BLACK))
            ind += 1

def draw_grid():
    SCREEN.fill(WHITE)
    for i in range(CELL_COUNT):
        cells[i].draw_cell(SCREEN)
    pygame.display.update()

def main():
    init_grid()
    running = True
    while running:
        clock.tick(FPS)
        draw_grid()

main()

pygame.quit()
