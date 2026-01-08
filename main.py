import pygame
import sys
import os
import src.settings
from src.settings import FPS, TITLU, COLORS, GRID_SIZE

# Importuri view si model
from src.view.popup import EditPopup
from src.view.interface import (
    draw_grid, draw_sidebar, draw_wires, draw_placed_components,
    VIEW_MENU_ITEMS, draw_simulation_results, SimulationButton
)
from src.model.circuit import Circuit
from src.model.elements import Resistor, VoltageSource, Capacitor, Transistor
from src.controller.connection import Connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "assets", "saves")
SAVE_FILE = os.path.join(SAVE_DIR, "circuit.json")

def main():
    pygame.init()

    # ensure folder exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    info_monitor = pygame.display.Info()
    src.settings.SIDEBAR_WIDTH = int(info_monitor.current_w * 0.20)

    FLAGS_FULLSCREEN = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((info_monitor.current_w, info_monitor.current_h), FLAGS_FULLSCREEN)

    pygame.display.set_caption(TITLU)
    clock = pygame.time.Clock()

    my_circuit = Circuit()
    connection = Connection(my_circuit)

    popup = EditPopup(info_monitor.current_w, info_monitor.current_h)

    # simulation buttons
    simulation_results = None
    button_width = 150
    button_height = 50
    button_margin = 20

    simulate_button = SimulationButton(
        src.settings.SIDEBAR_WIDTH + button_margin,
        info_monitor.current_h - button_height - button_margin,
        button_width,
        button_height,
        "SIMULARE"
    )

    reset_button = SimulationButton(
        src.settings.SIDEBAR_WIDTH + button_margin * 2 + button_width,
        info_monitor.current_h - button_height - button_margin,
        button_width,
        button_height,
        "RESET"
    )

    count_res = 1
    count_volt = 1
    count_cap = 1
    count_tran = 1

    dragged_component = None
    last_click_time = 0
    double_click_threshold = 500
    offset_x = 0
    offset_y = 0

    running = True

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        simulate_button.update(mouse_pos)
        reset_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if popup.active:
                action = popup.handle_event(event)
                if action == "save":
                    popup.apply_changes()
                    popup.close()
                elif action == "delete":
                    connection.disconnect_component(popup.component)
                    if popup.component in my_circuit.components:
                        my_circuit.components.remove(popup.component)
                    popup.close()
                elif action == "cancel":
                    popup.close()
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    connection.toggle_wire_mode()

                elif event.key == pygame.K_r:
                    if dragged_component:
                        dragged_component.rotate()

                elif event.key == pygame.K_s:
                    from src.controller.circuit_load import save_circuit
                    save_circuit(SAVE_FILE, my_circuit, connection)
                    print(f"Saved circuit to {SAVE_FILE}")

                elif event.key == pygame.K_l:
                    from src.controller.circuit_load import load_circuit
                    my_circuit, connection = load_circuit(SAVE_FILE)
                    simulation_results = None
                    dragged_component = None
                    print(f"Loaded circuit from {SAVE_FILE}")



            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    if simulate_button.is_clicked(mouse_pos, True):
                        print("SIMULARE PORNITA...")
                        try:
                            from src.model.solver import Solver
                            solver = Solver(my_circuit)
                            simulation_results = solver.solve()
                        except Exception as e:
                            print(f"Eroare solver: {e}")
                        continue

                    if reset_button.is_clicked(mouse_pos, True):
                        simulation_results = None
                        print("Resetat.")
                        continue

                    if connection.wire_mode:
                        result = connection.handle_click(mx, my)
                        if result: continue

                    if mx < src.settings.SIDEBAR_WIDTH:
                        btn_y = 20
                        for item in VIEW_MENU_ITEMS:
                            btn_rect = pygame.Rect(5, btn_y, src.settings.SIDEBAR_WIDTH - 10, 50)
                            if btn_rect.collidepoint(mx, my):
                                zona_lucru = info_monitor.current_w - src.settings.SIDEBAR_WIDTH
                                cx = src.settings.SIDEBAR_WIDTH + (zona_lucru // 2)
                                cy = info_monitor.current_h // 2
                                cx = round(cx / GRID_SIZE) * GRID_SIZE
                                cy = round(cy / GRID_SIZE) * GRID_SIZE

                                new_obj = None
                                if item["nume"] == "Rezistor":
                                    new_obj = Resistor(f"R{count_res}", 1000, cx, cy)
                                    count_res += 1
                                elif item["nume"] == "Baterie":
                                    new_obj = VoltageSource(f"V{count_volt}", 9, cx, cy)
                                    count_volt += 1
                                elif item["nume"] == "Capacitor":
                                    new_obj = Capacitor(f"C{count_cap}", 0.00001, cx, cy)
                                    count_cap += 1
                                elif item["nume"] == "Tranzistor":
                                    new_obj = Transistor(f"Q{count_tran}", "NPN", cx, cy)
                                    count_tran += 1

                                if new_obj:
                                    new_obj.img_name = item["img"]
                                    new_obj.rect = pygame.Rect(cx - 20, cy - 20, 40, 40)
                                    my_circuit.add_component(new_obj)
                            btn_y += 60

                    else:
                        for comp in reversed(my_circuit.components):
                            if hasattr(comp, 'rect') and comp.rect.collidepoint(mx, my):
                                if current_time - last_click_time < double_click_threshold:
                                    popup.open(comp)
                                    dragged_component = None
                                    break

                                dragged_component = comp
                                offset_x = comp.rect.x - mx
                                offset_y = comp.rect.y - my
                                break
                        last_click_time = current_time

            elif event.type == pygame.MOUSEMOTION:
                if dragged_component:
                    mx, my = pygame.mouse.get_pos()
                    raw_x = mx + offset_x
                    raw_y = my + offset_y
                    new_x = round(raw_x / GRID_SIZE) * GRID_SIZE
                    new_y = round(raw_y / GRID_SIZE) * GRID_SIZE

                    dragged_component.x = new_x + 20
                    dragged_component.y = new_y + 20
                    dragged_component.rect.x = new_x
                    dragged_component.rect.y = new_y

            elif event.type == pygame.MOUSEBUTTONUP:
                dragged_component = None

        screen.fill(COLORS["BACKGROUND"])
        draw_grid(screen)
        draw_placed_components(screen, my_circuit, connection)
        draw_wires(screen, connection, simulation_results, pygame.time.get_ticks())
        draw_sidebar(screen)

        simulate_button.draw(screen)
        reset_button.draw(screen)

        if simulation_results and simulation_results["success"]:
            draw_simulation_results(screen, my_circuit, simulation_results)

        if connection.wire_mode:
            font = pygame.font.Font(None, 36)
            text = font.render("WIRE MODE: ON", True, (0, 255, 0))
            screen.blit(text, (src.settings.SIDEBAR_WIDTH + 10, 10))
            inst_surf = pygame.font.Font(None, 20).render("Click 2 pini | W = exit", True, (255, 255, 255))
            inst_rect = inst_surf.get_rect(topleft=(src.settings.SIDEBAR_WIDTH + 10, 50))
            pygame.draw.rect(screen, (0, 0, 0), inst_rect.inflate(10, 5))
            screen.blit(inst_surf, inst_rect)

        if popup.active:
            popup.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()