import pygame
from src.settings import GRID_SIZE, COLORS
def draw_grid(screen):

    latime_reala = screen.get_width()
    inaltime_reala = screen.get_height()

    for x in range(0, latime_reala, GRID_SIZE):
        for y in range(0, inaltime_reala, GRID_SIZE):
            pygame.draw.circle(screen, COLORS["DOTS"], (x, y), 2)