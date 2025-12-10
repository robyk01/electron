import pygame
import sys

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLU, COLORS
from src.view.interface import draw_grid

def main():
    pygame.init()

    # CITIM DIMENSIUNEA MONITORULUI
    info_monitor = pygame.display.Info()
    MONITOR_W = info_monitor.current_w
    MONITOR_H = info_monitor.current_h

    FLAGS_FULLSCREEN = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    # pygame fullscreen scoate bara de sus
    # pygame hwsurface face ca aplicatia sa ruleze pe GPU nu CPU
    # DOUBLEBUF face doua ecrane, totul se deseneaza intre timp pe cel din spate si la flip ne arata rezultatul

    screen = pygame.display.set_mode((MONITOR_W, MONITOR_H), FLAGS_FULLSCREEN)

    pygame.display.set_caption(TITLU)
    clock = pygame.time.Clock()

    running = True
    is_fullscreen = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Posibilitatea de a ieși din Fullscreen (ESC sau F11)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11 or event.key == pygame.K_ESCAPE:
                    is_fullscreen = not is_fullscreen

                    if is_fullscreen:
                        screen = pygame.display.set_mode((MONITOR_W, MONITOR_H), FLAGS_FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            # (Aici vin adaugate clikcuri pe piese, mai dureaza)

        # Desenare
        screen.fill(COLORS["BACKGROUND"])
        draw_grid(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()