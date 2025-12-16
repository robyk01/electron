import pygame
import sys
import src.settings
# ### MODIFICARE 1: Am adaugat GRID_SIZE in lista de importuri
from src.settings import FPS, TITLU, COLORS, GRID_SIZE

# Importuri view si model
from src.view.interface import draw_grid, draw_sidebar, draw_wires, draw_placed_components, VIEW_MENU_ITEMS
from src.model.circuit import Circuit
from src.model.elements import Resistor, VoltageSource, Capacitor, Transistor
from src.controller.connection import Connection


def main():
    pygame.init()

    info_monitor = pygame.display.Info()
    src.settings.SIDEBAR_WIDTH = int(info_monitor.current_w * 0.20)

    FLAGS_FULLSCREEN = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

    # pygame fullscreen scoate bara de sus
    # pygame hwsurface face ca aplicatia sa ruleze pe GPU nu CPU
    # DOUBLEBUF face doua ecrane, totul se deseneaza intre timp pe cel din spate si la flip ne arata rezultatul
    # | operatie binara pe flaguri, ca sa le avem pe toate 3 setate simultan.

    screen = pygame.display.set_mode((info_monitor.current_w, info_monitor.current_h), FLAGS_FULLSCREEN)
    # screen = pygame.display.set_mode((1280, 720)) 
    pygame.display.set_caption(TITLU)
    clock = pygame.time.Clock()

    my_circuit = Circuit()
    connection = Connection(my_circuit)
    # Count ca sa putem avea mai multe piese de acelasi tip cu rezistente si chestii diferite
    count_res = 1
    count_volt = 1
    count_cap = 1
    count_tran = 1

    dragged_component = None
    offset_x = 0
    offset_y = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_w:
                    connection.toggle_wire_mode() # toggle wire mode by pressing 'w'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # in pygame 1 e click stanga
                    mx, my = pygame.mouse.get_pos()

                    # check wire mode
                    if connection.wire_mode:
                        result = connection.handle_click(mx, my)
                        if result:
                            continue

                    # Prima data verificam daca clickul a fost in meniu
                    if mx < src.settings.SIDEBAR_WIDTH:
                        btn_y = 20

                        for item in VIEW_MENU_ITEMS:
                            btn_rect = pygame.Rect(5, btn_y, src.settings.SIDEBAR_WIDTH - 10, 50)
                            # se creaza un dreptunghi exact pe pozitiile butoanelor din meniu
                            if btn_rect.collidepoint(mx, my):
                                # verificam daca clickul este in acest dreptunghi
                                # daca da, verificam pe ce tip de obiect am dat click si il creem

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
                                    # Pastram centrarea vizuala (-20), dar baza cx, cy e acum pe grila
                                    new_obj.rect = pygame.Rect(cx - 20, cy - 20, 40, 40)
                                    my_circuit.add_component(new_obj)

                            btn_y += 60  # 50 inaltime + 10 padding

                    # Daca clickul nu a fost in meniu, a fost pe masa de lucru, aaa ca vedem daca este pe pozitia vreounei
                    # componente si daca dam click pe ea incepem actiunea de drag and drop
                    else:
                        for comp in reversed(my_circuit.components):
                            # in reversed() ca sa folosim principiul unei stive, daca avem mai multe piese una peste alta
                            # o luam pe cea de deasupra
                            if hasattr(comp, 'rect') and comp.rect.collidepoint(mx, my):
                                dragged_component = comp
                                offset_x = comp.rect.x - mx
                                offset_y = comp.rect.y - my
                                break

            elif event.type == pygame.MOUSEMOTION:
                if dragged_component:  # executam doar daca am dat click pe o piesa din worktable
                    mx, my = pygame.mouse.get_pos()

                    # Calculam pozitia cu SNAP TO GRID
                    raw_x = mx + offset_x
                    raw_y = my + offset_y

                    # mutam prima data ce este vizual
                    new_x = round(raw_x / GRID_SIZE) * GRID_SIZE
                    new_y = round(raw_y / GRID_SIZE) * GRID_SIZE

                    dragged_component.x = new_x + 20  # actualizam self.x si self.y la componenta
                    dragged_component.y = new_y + 20

                    dragged_component.rect.x = new_x
                    dragged_component.rect.y = new_y

            elif event.type == pygame.MOUSEBUTTONUP:
                dragged_component = None

        screen.fill(COLORS["BACKGROUND"])
        draw_grid(screen)
        draw_placed_components(screen, my_circuit, connection)
        draw_wires(screen, connection)
        draw_sidebar(screen)

        # wire mode visual indicator
        if connection.wire_mode:
            font = pygame.font.Font(None, 36)
            text = font.render("WIRE MODE: ON", True, (0, 255, 0))
            screen.blit(text, (src.settings.SIDEBAR_WIDTH + 10, 10))
            
            font_small = pygame.font.Font(None, 20)
            inst_text = "Click 2 pini pentru conectare | W = exit"
            inst_surf = font_small.render(inst_text, True, (255, 255, 255))  
            
            inst_rect = inst_surf.get_rect(topleft=(src.settings.SIDEBAR_WIDTH + 10, 50))
            pygame.draw.rect(screen, (0, 0, 0), inst_rect.inflate(10, 5))  
            screen.blit(inst_surf, inst_rect)


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()