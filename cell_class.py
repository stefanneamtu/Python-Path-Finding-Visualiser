import pygame

class Cell:
    
    def __init__(self, rectangle, colour):
        self.rectangle = rectangle
        self.colour = colour
        self.is_wall = False

    def change_colour(self, colour):
        self.colour = colour

    def draw_cell(self, screen):
        pygame.draw.rect(screen, self.colour, self.rectangle, 1)

    def on_click():
        self.is_wall = not self.is_wall
