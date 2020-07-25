import pygame

class Colours:
    WHITE = (255, 255, 255) # Free cell
    BLACK = (0, 0, 0)       # Obstacle cell
    CYAN = (0, 255, 255)    # Start cell
    ORANGE = (255, 69, 0)   # End cell
    BLUE = (30, 144, 255)   # Path cell
    GREEN = (0, 255, 0)     # Visited cell
    RED = (220, 20, 60)     # Visited border cell
    GREY = (192, 192, 192)  # Border cell

class Cell:
    
    def __init__(self, rectangle, colour, x, y):
        self.rectangle = rectangle
        self.colour = colour
        self.is_wall = False
        self.x = x
        self.y = y

    def get_coords(self):
        return (self.x, self.y)

    def get_heuristic_value(self, end_cell):
        x, y = end_cell.get_coords()
        return abs(x - self.x) + abs(y - self.y)

    def change_colour(self, colour):
        self.colour = colour

    def draw_cell(self, screen):
        pygame.draw.rect(screen, self.colour, self.rectangle, 0)

    def on_click(self):
        self.is_wall = not self.is_wall

    def is_start(self):
        return self.colour == Colours.ORANGE

    def is_border(self):
        return self.colour == Colours.GREY

    def is_end(self):
        return self.colour == Colours.CYAN

    def is_obstacle(self):
        return self.colour == Colours.BLACK
    
    def is_visited(self):
        return self.colour == Colours.GREEN or self.colour == Colours.RED

    def make_start(self):
        self.colour = Colours.ORANGE

    def make_end(self):
        self.colour = Colours.CYAN

    def make_wall(self):
        self.colour = Colours.BLACK

    def reset_cell(self):
        self.colour = Colours.WHITE

    def __lt__(self, other):
        return False
