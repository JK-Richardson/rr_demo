# Ricochet Robots

This project is a Python implementation of the board game "Ricochet Robots," built using the `pygame` library.

NB: This was created as a learning project and not for any commercial use.

## Getting Started

To run this project locally, you'll need to have Python 3.12+ and `uv` installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/rr_demo.git
    cd rr_demo
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    uv sync
    ```

3.  **Run the game or solver:**

    ```bash
    uv run python main.py [--solve] [--seed SEED]
    ```

    - `--solve`: Runs the solver algorithm instead of the interactive game loop.
    - `--seed SEED`: Sets the random seed for reproducible board and robot placement. Replace `SEED` with any integer value.

## Building from Source

If you want to create a standalone executable that can be run without installing Python or any dependencies, you can build it using PyInstaller.

1.  **Install development dependencies:**

    Make sure you have completed the "Getting Started" steps first, then run:

    ```bash
    uv sync --all-extras
    ```

2.  **Build the executable:**

    ```bash
    uv run pyinstaller --onefile --name rr_demo main.py
    ```

    This will create a single executable file named `rr_demo` in the `dist` directory.

## How to Play
## Command Line Parameters

You can control the game and solver behavior using these command line options:

- `--solve`: Run the solver to automatically find a solution for the current board and target.
- `--seed SEED`: Specify a random seed to ensure reproducible board and robot placement.

Example:

```bash
uv run python main.py --solve --seed 42
```

The goal of the game is to move the robots on the board to reach a specific target cell. The robots move in a straight line until they hit a wall or another robot.

- Use the number keys (1-4) to select a robot.
- Use the arrow keys (Up, Down, Left, Right) to move the selected robot.
- The selected robot will move in the chosen direction until it is blocked by a wall or another robot.
- The objective is to get the correct colored robot to the target cell in as few moves as possible.
- Press 'r' to reset the board to its initial state.

## Project Structure

* `main.py`: Entry point for running the game or solver. Handles command line arguments.
* `board.yaml`: Configuration file for the game board layout.
* `src/`: Core source code for the game and solver.
    * `game.py`: Main game logic, including the game loop, input handling, and rendering.
    * `board.py`: Defines the game board, cells, walls, and targets.
    * `robots.py`: Defines robot objects and their movement logic.
    * `common.py`: Common data structures, enums, and constants.
    * `utils.py`: Utility functions, such as logging setup.
    * `solver.py`: Implements the solver algorithm for finding solutions automatically.
* `tests/`: Unit tests for the project.
## Solver

The solver is implemented in `src/solver.py` and can be invoked using the `--solve` command line parameter. It explores the state space of the board using a breadth-first search (BFS) algorithm to find a sequence of moves that solves the puzzle.

**Features:**
- Explores all possible robot moves to find a solution.
- Each state is represented by the positions of all robots.
- Returns a solution object containing the sequence of moves.
- Can be used with a random seed for reproducible results.

**Usage:**

```bash
uv run python main.py --solve [--seed SEED]
```

When run, the solver will print or return the solution path for the current board and target configuration.
