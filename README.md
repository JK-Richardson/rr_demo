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

3.  **Run the game:**

    ```bash
    uv run python main.py
    ```

## Building from Source

If you want to create a standalone executable that can be run without installing Python or any dependencies, you can build it using PyInstaller.

1.  **Install development dependencies:**

    Make sure you have completed the "Getting Started" steps first, then run:

    ```bash
    uv sync --dev
    ```

2.  **Build the executable:**

    ```bash
    uv run build
    ```

    This will create a single executable file in the `dist` directory.

## How to Play

The goal of the game is to move the robots on the board to reach a specific target cell. The robots move in a straight line until they hit a wall or another robot.

- Use the number keys (1-4) to select a robot.
- Use the arrow keys (Up, Down, Left, Right) to move the selected robot.
- The selected robot will move in the chosen direction until it is blocked by a wall or another robot.
- The objective is to get the correct colored robot to the target cell in as few moves as possible.
- Press 'r' to reset the board to its initial state.

## Project Structure

- `main.py`: The entry point for the game.
- `board.yaml`: Configuration file for the game board layout.
- `src/`: Contains the core source code for the game.
  - `game.py`: Main game logic, including the game loop, input handling, and rendering.
  - `board.py`: Defines the game board, cells, walls, and targets.
  - `robots.py`: Defines the robot objects and their movement logic.
  - `common.py`: Contains common data structures and constants.
  - `utils.py`: Utility functions, such as logging setup.
- `tests/`: Contains unit tests for the project.
