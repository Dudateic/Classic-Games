import pygame
from game import Game
pygame.init() 

SCREEN_WIDTH  = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
TITLE         = "Space Invaders"


def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    Game(screen).run()
    pygame.quit()


if __name__ == "__main__":
    main()
