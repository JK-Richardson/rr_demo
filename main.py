import pathlib

import pygame

from src.game import Game
from src.utils import setup_logging

if __name__ == "__main__":
    setup_logging()
    pygame.init()
    game = Game(config_path=pathlib.Path("./board.yaml"))
    game.run()
    pygame.quit()
