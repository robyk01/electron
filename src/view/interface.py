import pygame
import os
import src.settings
from src.settings import COLORS, GRID_SIZE
from src.model.base import Component

from src.model.elements import Transistor


pygame.font.init()
MENU_FONT = pygame.font.SysFont("Arial", 24)

LOADED_IMAGES = {}

VIEW_MENU_ITEMS = [
    {"nume": "Rezistor", "img": "rezistor.png"},
    {"nume": "Baterie", "img": "baterie.png"},
    {"nume": "Capacitor", "img": "capacitor.png"},
    {"nume": "Tranzistor", "img": "tranzistor.png"},
]


def get_image(nume_fisier):
    if nume_fisier in LOADED_IMAGES:
        return LOADED_IMAGES[nume_fisier]
    cale = os.path.join("assets", "icons", nume_fisier)
    try:
        img = pygame.image.load(cale).convert_alpha()
    except:
        return None
    LOADED_IMAGES[nume_fisier] = img
    return img


def draw_grid(screen):
    w = screen.get_width()
    h = screen.get_height()
    for x in range(src.settings.SIDEBAR_WIDTH, w, GRID_SIZE):
        for y in range(0, h, GRID_SIZE):
            pygame.draw.circle(screen, COLORS["DOTS"], (x, y), 2)


def draw_sidebar(screen):
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
            original_img = get_image(comp.img_name)

            if original_img:
                rotated_img = pygame.transform.rotate(original_img, comp.rotation)
                new_rect = rotated_img.get_rect(center=comp.rect.center)
                screen.blit(rotated_img, new_rect.topleft)

            if connection and connection.wire_mode:
                pin_positions = comp.get_pin_positions()

                pin_labels = []
                if isinstance(comp, Transistor):
                    pin_labels = ["C", "B", "E"]

                for i, (px, py) in enumerate(pin_positions):
                    pin_color = (255, 0, 0)  # red
                    pin_radius = 5

                    if (comp == connection.wire_start_component and i == connection.wire_start_pin):
                        pin_color = (0, 255, 0)  # green
                        pin_radius = 7

                    pygame.draw.circle(screen, pin_color, (int(px), int(py)), pin_radius)
                    pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), pin_radius - 2)

                    if pin_labels and i < len(pin_labels):
                        label_font = pygame.font.Font(None, 16)
                        label = label_font.render(pin_labels[i], True, (255, 255, 255))
                        screen.blit(label, (int(px) + 8, int(py) - 8))


def _vec2(p):
    return pygame.Vector2(float(p[0]), float(p[1]))


def _draw_flow_particles_on_segment(screen, a, b, t_ms: int, color=(0, 220, 255), thickness=3):
    a = _vec2(a)
    b = _vec2(b)
    seg = b - a
    length = seg.length()
    if length < 1:
        return

    speed_px_s = 180.0
    dot_count = 8
    dot_radius = 3
    pad = 6.0

    usable = max(1.0, length - 2 * pad)
    phase = ((t_ms / 1000.0) * speed_px_s / length) % 1.0
    dirv = seg / length

    for k in range(dot_count):
        u = (k / dot_count + phase) % 1.0
        dist = pad + u * usable
        p = a + dirv * dist
        pygame.draw.circle(screen, color, (int(p.x), int(p.y)), dot_radius)

def draw_wires(screen, connection, results=None, t_ms: int = 0, active_wire_indices=None):
    if not connection:
        return

    wire_color = (50, 50, 50)
    wire_thickness = 3

    node_voltages = None
    component_currents = {}

    if results and isinstance(results, dict) and results.get("success"):
        node_voltages = results.get("node_voltages", {})
        component_currents = results.get("component_currents", {})

    if active_wire_indices is None and node_voltages is not None:
        active_wire_indices = []
        for i, (comp1, pin1, comp2, pin2) in enumerate(connection.wires):
            # check if there is voltage difference across this wire
            n1 = comp1.nodes[pin1] if pin1 < len(comp1.nodes) else None
            n2 = comp2.nodes[pin2] if pin2 < len(comp2.nodes) else None
            
            if n1 is not None and n2 is not None:
                v1 = node_voltages.get(n1, 0.0)
                v2 = node_voltages.get(n2, 0.0)
                
                # check if components connected to this wire have current
                current1 = abs(component_currents.get(comp1.uuid, 0))
                current2 = abs(component_currents.get(comp2.uuid, 0))
                
                # animate if: voltage difference or component has current > 0.1mA
                if abs(v1 - v2) > 0.01 or current1 > 0.0001 or current2 > 0.0001:
                    active_wire_indices.append(i)

    if active_wire_indices is None:
        active_wire_indices = []


    # Folosim enumerate ca sa stim indexul firului (0, 1, 2...)
    for i, (comp1, pin1, comp2, pin2) in enumerate(connection.wires):
        try:
            if comp1 in connection.circuit.components and comp2 in connection.circuit.components:
                pos1 = comp1.get_pin_positions()[pin1]
                pos2 = comp2.get_pin_positions()[pin2]

                pygame.draw.line(screen, wire_color, pos1, pos2, wire_thickness)

                # desenem animatia doar daca firul este in queue
                if i in active_wire_indices:
                    n1 = comp1.nodes[pin1]
                    n2 = comp2.nodes[pin2]
                    if n1 is None or n2 is None:
                        continue

                    v1 = node_voltages.get(n1, 0.0) if node_voltages else 0.0
                    v2 = node_voltages.get(n2, 0.0) if node_voltages else 0.0

                    # determine flow direction (high voltage to low)
                    # if same voltage, use component current direction
                    if v1 >= v2:
                        a, b = pos1, pos2
                    else:
                        a, b = pos2, pos1
                        
                    _draw_flow_particles_on_segment(screen, a, b, t_ms, color=(0, 220, 255))
        except:
            continue

    if connection.wire_mode and connection.wire_start_component:
        try:
            start_pos = connection.wire_start_component.get_pin_positions()[connection.wire_start_pin]
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 0, 0), start_pos, (mx, my), 2)
        except:
            pass


class SimulationButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color_normal = (50, 150, 50)
        self.color_hover = (70, 200, 70)
        self.color_active = (30, 100, 30)
        self.is_hovered = False
        self.is_pressed = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        if self.is_pressed:
            color = self.color_active
        elif self.is_hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        font = pygame.font.Font(None, 28)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos) and mouse_pressed:
            self.is_pressed = True
            return True
        self.is_pressed = False
        return False


def draw_simulation_results(screen, circuit, results):
    font_title = pygame.font.Font(None, 32)
    font_data = pygame.font.Font(None, 20)

    title = font_title.render("REZULTATE SIMULARE", True, (0, 255, 0))
    title_x = screen.get_width() - 300
    title_y = 15
    title_rect = title.get_rect(topleft=(title_x, title_y))
    pygame.draw.rect(screen, (0, 0, 0), title_rect.inflate(20, 10))
    screen.blit(title, title_rect)

    node_voltages = results.get("node_voltages", {})
    component_currents = results.get("component_currents", {})
    transistor_states = results.get("transistor_states", {}) 

    for comp in circuit.components:
        box_x = comp.x + 55
        box_y = comp.y - 15

        info_lines = []
        for i, node_id in enumerate(comp.nodes):
            if node_id is not None:
                voltage = node_voltages.get(node_id, 0)
                info_lines.append((f"Pin{i}: {voltage:.2f}V", (255, 200, 0)))

        current = component_currents.get(comp.uuid, 0)
        current_ma = abs(current) * 1000

        if current_ma < 1:
            color = (0, 255, 0)
        elif current_ma < 50:
            color = (255, 255, 0)
        elif current_ma < 100:
            color = (255, 165, 0)
        else:
            color = (255, 0, 0)

        info_lines.append((f"I: {current_ma:.2f}mA", color))

        max_width = max([font_data.size(line[0])[0] for line in info_lines]) if info_lines else 100
        box_height = len(info_lines) * 22 + 10

        pygame.draw.rect(screen, (0, 0, 0), (box_x - 5, box_y - 5, max_width + 15, box_height))
        pygame.draw.rect(screen, (100, 100, 100), (box_x - 5, box_y - 5, max_width + 15, box_height), 2)

        current_y = box_y
        for line_text, line_color in info_lines:
            text = font_data.render(line_text, True, line_color)
            screen.blit(text, (box_x, current_y))
            current_y += 22

    from src.model.elements import Transistor
    for comp in circuit.components:
        if isinstance(comp, Transistor):
            state = transistor_states.get(comp.uuid, False)

            # green if ON, red if OFF
            color = (0, 255, 0) if state else (255, 0, 0)
            status_text = "ON" if state else "OFF"

            font = pygame.font.Font(None, 24)
            label = font.render(status_text, True, color)

            label_rect = label.get_rect(center=(comp.rect.centerx, comp.rect.top - 25))
            pygame.draw.rect(screen, (0, 0, 0), label_rect.inflate(10, 6))
            
            screen.blit(label, label_rect)