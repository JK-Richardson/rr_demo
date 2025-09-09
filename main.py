import pygame
from game import Game
from utils import setup_logging

if __name__ == '__main__':
    setup_logging()
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()