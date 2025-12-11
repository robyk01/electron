import pygame
import sys
import src.settings
from src.settings import FPS, TITLU, COLORS
from src.view.interface import draw_grid, draw_sidebar


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

    pygame.display.set_caption(TITLU)
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # (Aici vin adaugate clikcuri pe piese, mai dureaza)

        screen.fill(COLORS["BACKGROUND"])
        draw_grid(screen)
        draw_sidebar(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()