import argparse
import pathlib
import random
import sys

import src.solver as solver
from src.game import Game
from src.utils import setup_logging


def get_config_path() -> pathlib.Path:
    """Returns the path to the board.yaml file."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running in a PyInstaller bundle
        return pathlib.Path(sys._MEIPASS) / "board.yaml"  # type: ignore
    else:
        # Running as a script
        return pathlib.Path("./board.yaml")


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Ricochet Robots Benchmark")
    parser.add_argument(
        "--startSeed",
        type=int,
        default=0,
        help="Start seed for the benchmark",
    )
    parser.add_argument(
        "--endSeed",
        type=int,
        default=10,
        help="End seed for the benchmark",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable profiling for the solver",
    )
    args = parser.parse_args()

    if args.profile:
        import cProfile
        import pstats

        print(f"Profiling solver with seed {args.startSeed}...")
        random.seed(args.startSeed)
        game = Game(config_path=get_config_path())
        solver_instance = solver.Solver(game)

        profiler = cProfile.Profile()
        profiler.enable()
        solution = solver_instance.solve()
        profiler.disable()

        print(f"Solution found with {len(solution.moves)} moves.")
        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats()
        sys.exit(0)

    longest_solution = []
    longest_solution_seed = -1

    for seed in range(args.startSeed, args.endSeed + 1):
        print(f"Solving for seed {seed}...")
        random.seed(seed)
        game = Game(config_path=get_config_path())
        solver_instance = solver.Solver(game)
        solution = solver_instance.solve()

        if len(solution.moves) > len(longest_solution):
            longest_solution = solution.moves
            longest_solution_seed = seed

    print("\n--- Benchmark Complete ---")
    print(f"Longest solution found with seed: {longest_solution_seed}")
    print(f"Number of moves: {len(longest_solution)}")
    print(f"Solution: {longest_solution}")
