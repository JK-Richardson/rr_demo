import pathlib
import random
from typing import Any  # Import Any for type hinting

import pygame
import yaml
import pandas as pd

from .common import (  # Import Target, TargetShape, TARGET_SHAPES, TARGET_COLORS from common.py
    TARGET_COLORS,
    TARGET_SHAPES,
    Target,
    TargetShape,
)


class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.has_wall_north = False
        self.has_wall_east = False
        self.has_wall_south = False
        self.has_wall_west = False
        self.target = None


def draw_target_shape(
    screen: pygame.Surface,
    target_shape: TargetShape,
    target_color: tuple[int, int, int],
    center_x: int,
    center_y: int,
    scale: int,
) -> None:
    if target_shape == TargetShape.CIRCLE:
        pygame.draw.circle(screen, target_color, (center_x, center_y), scale // 2)
    elif target_shape == TargetShape.SQUARE:
        side = scale // 1.5
        square_rect = pygame.Rect(
            center_x - side // 2, center_y - side // 2, side, side
        )
        pygame.draw.rect(screen, target_color, square_rect)
    elif target_shape == TargetShape.TRIANGLE:
        point1 = (center_x, center_y - scale // 3)
        point2 = (center_x - scale // 3, center_y + scale // 3)
        point3 = (center_x + scale // 3, center_y + scale // 3)
        pygame.draw.polygon(screen, target_color, [point1, point2, point3])
    elif target_shape == TargetShape.ELLIPSE:
        ellipse_rect = pygame.Rect(
            center_x - scale // 3, center_y - scale // 4, 2 * scale // 3, 2 * scale // 4
        )
        pygame.draw.ellipse(screen, target_color, ellipse_rect)


class Board:
    def __init__(self, config_path: pathlib.Path) -> None:
        config = self._load_config(config_path)
        self.width: int = config["width"]
        self.height: int = config["height"]
        self.grid: list[list[Cell]] = self._create_empty_grid(self.width, self.height)
        self._target_lookup: dict[Target, tuple[int, int]] = {}

        self.grid_line_color: tuple[int, int, int] = tuple(
            config.get("grid_line_color", [200, 200, 200])
        )
        self.wall_color: tuple[int, int, int] = tuple(
            config.get("wall_color", [255, 0, 0])
        )
        self.show_cell_coords: bool = config.get("show_cell_coords", False)

        self.buffer = 50

        # Randomly assign target coordinates
        available_coords = [tuple(coord) for coord in config["target_coordinates"]]
        random.shuffle(available_coords)

        all_targets = list(Target)  # Get all target enums
        if len(available_coords) < len(all_targets):
            raise ValueError("Not enough unique coordinates for all targets.")

        for i, target_enum in enumerate(all_targets):
            row, col = available_coords[i]
            self.grid[row][col].target = target_enum
            self._target_lookup[target_enum] = (row, col)

        self._apply_walls(config)

        # Create and store the board layout as a DataFrame
        self.df: pd.DataFrame = self.to_dataframe()

    def get_target_coords(self, target: Target) -> tuple[int, int]:
        """Returns (row, col) for the given target"""
        return self._target_lookup[target]

    def _load_config(self, config_path: pathlib.Path) -> dict[str, Any]:
        with open(config_path, "r") as f:
            config: dict[str, Any] = yaml.safe_load(f)
        return config

    def _apply_walls(self, config: dict[str, Any]) -> None:
        # Apply outer border walls
        for r in range(self.height):
            self.grid[r][0].has_wall_west = True
            self.grid[r][self.width - 1].has_wall_east = True
        for c in range(self.width):
            self.grid[0][c].has_wall_north = True
            self.grid[self.height - 1][c].has_wall_south = True

        # Apply internal walls from config
        walls_config = config["walls"]
        for coord_str, wall_def in walls_config.items():
            # Convert string key "(row, col)" to tuple (row, col)
            row, col = map(int, coord_str.strip("()").split(","))
            cell = self.grid[row][col]
            # Set walls symmetrically for both the cell and its neighbor
            if "N" in wall_def:
                cell.has_wall_north = True
                if row > 0:
                    self.grid[row - 1][col].has_wall_south = True
            if "E" in wall_def:
                cell.has_wall_east = True
                if col < self.width - 1:
                    self.grid[row][col + 1].has_wall_west = True
            if "S" in wall_def:
                cell.has_wall_south = True
                if row < self.height - 1:
                    self.grid[row + 1][col].has_wall_north = True
            if "W" in wall_def:
                cell.has_wall_west = True
                if col > 0:
                    self.grid[row][col - 1].has_wall_east = True

    def _create_empty_grid(self, width: int, height: int) -> list[list[Cell]]:
        grid: list[list[Cell]] = []
        for r in range(height):
            row: list[Cell] = []
            for c in range(width):
                cell = Cell(r, c)
                row.append(cell)
            grid.append(row)
        return grid

    def draw(self, screen: pygame.Surface) -> None:
        cell_width: int = (screen.get_width() - 2 * self.buffer) // self.width
        cell_height: int = (screen.get_height() - 2 * self.buffer) // self.height

        # Draw grid lines
        for r in range(self.height):
            for c in range(self.width):
                x: int = self.buffer + c * cell_width
                y: int = self.buffer + r * cell_height
                # Draw horizontal grid line
                pygame.draw.line(
                    screen, self.grid_line_color, (x, y), (x + cell_width, y), 1
                )
                # Draw vertical grid line
                pygame.draw.line(
                    screen, self.grid_line_color, (x, y), (x, y + cell_height), 1
                )

        # Draw walls and targets
        for r in range(self.height):
            for c in range(self.width):
                cell = self.grid[r][c]
                x = self.buffer + c * cell_width
                y = self.buffer + r * cell_height

                if cell.has_wall_north:
                    pygame.draw.line(
                        screen, self.wall_color, (x, y), (x + cell_width, y), 4
                    )
                if cell.has_wall_east:
                    pygame.draw.line(
                        screen,
                        self.wall_color,
                        (x + cell_width, y),
                        (x + cell_width, y + cell_height),
                        4,
                    )
                if cell.has_wall_south:
                    pygame.draw.line(
                        screen,
                        self.wall_color,
                        (x, y + cell_height),
                        (x + cell_width, y + cell_height),
                        4,
                    )
                if cell.has_wall_west:
                    pygame.draw.line(
                        screen, self.wall_color, (x, y), (x, y + cell_height), 4
                    )

                if cell.target:
                    shape: TargetShape | None = TARGET_SHAPES.get(cell.target)
                    color: tuple[int, int, int] | None = TARGET_COLORS.get(cell.target)
                    if shape and color:
                        center_x: int = x + cell_width // 2
                        center_y: int = y + cell_height // 2
                        draw_target_shape(
                            screen, shape, color, center_x, center_y, cell_width
                        )

                if self.show_cell_coords:
                    _font = pygame.font.SysFont(None, 24)
                    text: pygame.Surface = _font.render(f"{r},{c}", True, (0, 0, 0))
                    screen.blit(text, (x + 5, y + 5))

    def to_dataframe(self) -> pd.DataFrame:
        """
        Exports the board's wall layout to a pandas DataFrame.

        The DataFrame contains the row and column for each cell, and binary indicators
        for the presence of a wall on each of its four sides.

        Returns:
            pd.DataFrame: A DataFrame with columns for row, col, and wall presence.
        """
        data = []
        for r in range(self.height):
            for c in range(self.width):
                cell = self.grid[r][c]
                data.append({
                    "row": r,
                    "col": c,
                    "wall_north": 1 if cell.has_wall_north else 0,
                    "wall_east": 1 if cell.has_wall_east else 0,
                    "wall_south": 1 if cell.has_wall_south else 0,
                    "wall_west": 1 if cell.has_wall_west else 0,
                })
        return pd.DataFrame(data)
