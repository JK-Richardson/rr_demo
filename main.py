import pathlib
import random

import pygame

from src.game import Game
from src.utils import setup_logging

if __name__ == "__main__":
    import argparse

    setup_logging()
    parser = argparse.ArgumentParser(description="Ricochet Robots Demo")
    parser.add_argument(
        "--solve",
        action="store_true",
        help="Solve the board instead of running the game loop",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed to control randomization",
    )
    args = parser.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    else:
        random.seed(10)
    pygame.init()
    game = Game(config_path=pathlib.Path("./board.yaml"))
    if args.solve:
        # Call your solve function here, e.g. game.solve()
        print(f"Solving the board... (seed={args.seed})")
        import src.solver as solver

        solver_instance = solver.Solver(game)
        solution = solver_instance.solve()
        print("Solution found:", solution)
        game.run()
    else:
        game.run()
    pygame.quit()
