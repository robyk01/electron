import pygame
import sys

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLU, COLORS
from src.view.interface import draw_grid


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLU)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # (Aici vin adaugate clikcuri pe piese, mai dureaza)

        # Desenare Ecran
        screen.fill(COLORS["BACKGROUND"])

        # Apelez functia importata din interface.py
        draw_grid(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()