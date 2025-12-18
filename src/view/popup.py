import pygame
from src.settings import COLORS


class EditPopup:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.width = 400
        self.height = 300
        self.rect = pygame.Rect((screen_w - self.width) // 2, (screen_h - self.height) // 2, self.width, self.height)

        self.active = False
        self.component = None
        self.input_text = ""
        self.attr_name = ""  # ex: "resistance", "voltage"

        # Fonturi
        self.font_title = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 20)

        # relative la fereastra, le calculam la draw
        self.btn_save = pygame.Rect(0, 0, 100, 40)
        self.btn_delete = pygame.Rect(0, 0, 100, 40)
        self.btn_cancel = pygame.Rect(0, 0, 100, 40)
        self.input_rect = pygame.Rect(0, 0, 200, 40)

    def open(self, component):
        self.component = component
        self.active = True

        if hasattr(component, "resistance"):
            self.attr_name = "resistance"
            self.input_text = str(component.resistance)
        elif hasattr(component, "voltage"):
            self.attr_name = "voltage"
            self.input_text = str(component.voltage)
        elif hasattr(component, "capacitance"):
            self.attr_name = "capacitance"
            self.input_text = str(component.capacitance)
        else:
            self.attr_name = "N/A"
            self.input_text = ""

    def close(self):
        self.active = False
        self.component = None

    def handle_event(self, event):
        if not self.active:
            return None

        # Tastam in casute
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                return "save"
            elif event.key == pygame.K_ESCAPE:
                return "cancel"
            else:
                # Permitem doar cifre si punct
                if event.unicode.isnumeric() or event.unicode == '.':
                    self.input_text += event.unicode

        # Comportament click pe butoane
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()

            # Daca dam click in afara ferestrei, o inchidem
            if not self.rect.collidepoint(mx, my):
                return "cancel"

            if self.btn_save.collidepoint(mx, my):
                return "save"
            if self.btn_delete.collidepoint(mx, my):
                return "delete"
            if self.btn_cancel.collidepoint(mx, my):
                return "cancel"

        return None

    def apply_changes(self):
        if self.component and self.attr_name != "N/A":
            try:
                val = float(self.input_text)
                # Daca e rezistenta o vrem int, altfel float
                if self.attr_name == "resistance":
                    val = int(val)

                setattr(self.component, self.attr_name, val)
                print(f"Updated {self.component.name} to {val}")
            except ValueError:
                print("Valoare invalida!")

    def draw(self, screen):
        if not self.active:
            return

        # Fundal overlay
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negru transparent
        screen.blit(overlay, (0, 0))

        # Fereastra popup in sine
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=12)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=12)  # Contur

        # Titlul
        title_surf = self.font_title.render(f"Editare: {self.component.name}", True, (255, 255, 255))
        screen.blit(title_surf, (self.rect.x + 20, self.rect.y + 20))

        # Casuta input
        self.input_rect.topleft = (self.rect.x + 100, self.rect.y + 80)
        pygame.draw.rect(screen, (255, 255, 255), self.input_rect, border_radius=5)

        val_surf = self.font_ui.render(self.input_text, True, (0, 0, 0))
        screen.blit(val_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

        #(Ohm, V, F)
        label_text = "Value:"
        if self.attr_name == "resistance":
            label_text = "Ohm:"
        elif self.attr_name == "voltage":
            label_text = "Volts:"
        elif self.attr_name == "capacitance":
            label_text = "Farads:"

        label_surf = self.font_ui.render(label_text, True, (200, 200, 200))
        screen.blit(label_surf, (self.rect.x + 20, self.rect.y + 90))

        # Redesenam butoanele
        # SAVE (Verde)
        self.btn_save.bottomright = (self.rect.right - 20, self.rect.bottom - 20)
        pygame.draw.rect(screen, (0, 200, 0), self.btn_save, border_radius=8)
        save_txt = self.font_ui.render("SAVE", True, (255, 255, 255))
        screen.blit(save_txt, (self.btn_save.x + 25, self.btn_save.y + 10))

        # CANCEL (Gri)
        self.btn_cancel.bottomright = (self.btn_save.left - 20, self.rect.bottom - 20)
        pygame.draw.rect(screen, (100, 100, 100), self.btn_cancel, border_radius=8)
        cancel_txt = self.font_ui.render("Cancel", True, (255, 255, 255))
        screen.blit(cancel_txt, (self.btn_cancel.x + 20, self.btn_cancel.y + 10))

        # DELETE (Rosu)
        self.btn_delete.bottomleft = (self.rect.left + 20, self.rect.bottom - 20)
        pygame.draw.rect(screen, (200, 0, 0), self.btn_delete, border_radius=8)
        del_txt = self.font_ui.render("DELETE", True, (255, 255, 255))
        screen.blit(del_txt, (self.btn_delete.x + 15, self.btn_delete.y + 10))