import pygame
import os
from src.settings import *

pygame.font.init()
MENU_FONT = pygame.font.SysFont("Arial", 16)

# Ca sa nu luam o imagine din /assets/imagini de mai multe ori, o stocam aici
LOADED_IMAGES = {}

# Lista pieselor temporara, pana terminam la /model
VIEW_MENU_ITEMS = [
    {"nume": "Rezistor", "img": "rezistor.png"},
    {"nume": "Baterie", "img": "baterie.png"},
    {"nume": "Capacitor", "img": "capacitor.png"},
    {"nume": "Tranzistor", "img": "tranzistor.png"},
    {"nume": "Fir Conex.", "img": "fir.png"},
]

def get_image(nume_fisier):
    if nume_fisier in LOADED_IMAGES:
        return LOADED_IMAGES[nume_fisier]
    cale = os.path.join("assets", "icons", nume_fisier)
    # Daca imaginea nu este in LOADED_IMAGES, o incarcam
    try:
        img = pygame.image.load(cale).convert_alpha()
        LOADED_IMAGES[nume_fisier] = img
        return img

def draw_grid(screen):
    w = screen.get_width()
    h = screen.get_height()
    for x in range(SIDEBAR_WIDTH, w, GRID_SIZE):
        for y in range(0, h, GRID_SIZE):
            pygame.draw.circle(screen, COLORS["DOTS"], (x, y), 2)