import pygame

from const.CONSTANTS import SCREEN_SIZE
from game import Game

if __name__ == '__main__':
    pygame.init()

    game = Game()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    game.run = True

    while game.run:
        pygame.display.flip()
        if pygame.event.wait().type == pygame.QUIT:
            game.run = False
