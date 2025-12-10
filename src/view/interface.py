import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, COLORS

def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            # pygame.draw.circle(surface, color, center, radius) - documentatie pygame
            pygame.draw.circle(screen, COLORS["DOTS"], (x, y), 2)