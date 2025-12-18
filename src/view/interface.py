import pygame
import os
# IMPORTAM MODULUL COMPLET pentru a vedea modificarile facute in main.py (latimea dinamica)
import src.settings
from src.settings import COLORS, GRID_SIZE
from src.model.base import Component

pygame.font.init()
MENU_FONT = pygame.font.SysFont("Arial", 24)

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
    img = pygame.image.load(cale).convert_alpha()
    LOADED_IMAGES[nume_fisier] = img
    return img


def draw_grid(screen):
    w = screen.get_width()
    h = screen.get_height()

    for x in range(src.settings.SIDEBAR_WIDTH, w, GRID_SIZE):
        for y in range(0, h, GRID_SIZE):
            pygame.draw.circle(screen, COLORS["DOTS"], (x, y), 2)


def draw_sidebar(screen):
    # Am scos parametrul 'selected_comp' pentru ca acum avem Popup!
    sb_width = src.settings.SIDEBAR_WIDTH
    sb_height = screen.get_height()

    pygame.draw.rect(screen, COLORS["SIDEBAR_BG"], (0, 0, sb_width, sb_height))

    button_x = 5
    button_y = 20
    button_w = sb_width - 10
    button_h = 50
    padding = 10
    ICON_SIZE = 40

    for item in VIEW_MENU_ITEMS:
        btn_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        pygame.draw.rect(screen, COLORS["BUTTON_BG"], btn_rect, border_radius=8)

        img = get_image(item["img"])
        icon_x = button_x + 5
        icon_y = button_y + 5

        if img:
            screen.blit(img, (icon_x, icon_y))

        text_surf = MENU_FONT.render(item["nume"], True, COLORS["TEXT_WHITE"])
        text_x = button_x + ICON_SIZE + 20
        text_y = button_y + (button_h - text_surf.get_height()) // 2

        screen.blit(text_surf, (text_x, text_y))
        button_y += button_h + padding

def draw_placed_components(screen, circuit_obj, connection=None):

    if not circuit_obj:
        return

    for comp in circuit_obj.components:
        if hasattr(comp, "img_name") and hasattr(comp, "rect"):
            img = get_image(comp.img_name)
            if img:
                screen.blit(img, (comp.rect.x, comp.rect.y))

            # draw pins
            if connection and connection.wire_mode:
                pin_positions = comp.get_pin_positions()

                for i, (px, py) in enumerate(pin_positions):
                    pin_color = (255, 0, 0) # red
                    pin_radius = 5

                    if (comp == connection.wire_start_component and i == connection.wire_start_pin):
                        pin_color = (0, 255, 0) # green (selected)
                        pin_radius = 7
                    
                    # draw pin
                    pygame.draw.circle(screen, pin_color, (int(px), int(py)), pin_radius)

                    # draw white circle
                    pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), pin_radius - 2)

# draw wires between connected components
def draw_wires(screen, connection):
    if not connection:
        return
    
    wire_color = (50, 50, 50) # grey
    wire_thickness = 3

    for comp1, pin1, comp2, pin2 in connection.wires:
        pos1 = comp1.get_pin_positions()[pin1]
        pos2 = comp2.get_pin_positions()[pin2]

        pygame.draw.line(screen, wire_color, pos1, pos2, wire_thickness)

    # temporary line while in wire mode
    if connection.wire_mode and connection.wire_start_component:
        start_pos = connection.wire_start_component.get_pin_positions()[connection.wire_start_pin]
        mx, my = pygame.mouse.get_pos()

        pygame.draw.line(screen, (255, 0, 0), start_pos, (mx, my), 2)