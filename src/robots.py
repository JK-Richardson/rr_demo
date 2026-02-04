import pygame

from .board import Board  # Import Board for type hinting
from .common import (  # Import Direction, RobotColor, ROBOT_COLORS from common.py
    ROBOT_COLORS,
    Direction,
    RobotColor,
)


class Robot:
    def __init__(self, color: RobotColor, row: int, col: int) -> None:
        self.color = color
        self.row = row
        self.col = col

    def _is_robot_at(self, row: int, col: int, all_robots: list["Robot"]) -> bool:
        for robot in all_robots:
            if robot != self and robot.row == row and robot.col == col:
                return True
        return False

    def get_position(self) -> tuple[int, int]:
        return self.row, self.col

    def move(self, direction: Direction, board: Board, all_robots: list["Robot"]) -> None:
        """
        Moves the robot in the given direction until it hits a wall or another robot.
        The robot's position is updated in place. This version uses the board's
        DataFrame for efficient, vectorized obstacle detection.
        """
        df = board.df
        other_robots_pos = {
            (r.row, r.col) for r in all_robots if r is not self
        }

        if direction == Direction.UP:
            # Find walls in the path (cells with a north wall)
            path_df = df[(df["col"] == self.col) & (df["row"] < self.row) & (df["wall_north"] == 1)]
            wall_rows = path_df["row"]
            wall_stop_row = wall_rows.max() if not wall_rows.empty else 0

            # Find other robots in the path
            robot_rows = [r for r, c in other_robots_pos if c == self.col and r < self.row]
            robot_stop_row = max(robot_rows) if robot_rows else -1

            final_robot_stop = robot_stop_row + 1 if robot_stop_row != -1 else 0
            self.row = max(wall_stop_row, final_robot_stop)

        elif direction == Direction.DOWN:
            path_df = df[(df["col"] == self.col) & (df["row"] > self.row) & (df["wall_south"] == 1)]
            wall_rows = path_df["row"]
            wall_stop_row = wall_rows.min() if not wall_rows.empty else board.height - 1

            robot_rows = [r for r, c in other_robots_pos if c == self.col and r > self.row]
            robot_stop_row = min(robot_rows) if robot_rows else board.height

            final_robot_stop = robot_stop_row - 1 if robot_stop_row != board.height else board.height - 1
            self.row = min(wall_stop_row, final_robot_stop)

        elif direction == Direction.LEFT:
            path_df = df[(df["row"] == self.row) & (df["col"] < self.col) & (df["wall_west"] == 1)]
            wall_cols = path_df["col"]
            wall_stop_col = wall_cols.max() if not wall_cols.empty else 0

            robot_cols = [c for r, c in other_robots_pos if r == self.row and c < self.col]
            robot_stop_col = max(robot_cols) if robot_cols else -1

            final_robot_stop = robot_stop_col + 1 if robot_stop_col != -1 else 0
            self.col = max(wall_stop_col, final_robot_stop)

        elif direction == Direction.RIGHT:
            path_df = df[(df["row"] == self.row) & (df["col"] > self.col) & (df["wall_east"] == 1)]
            wall_cols = path_df["col"]
            wall_stop_col = wall_cols.min() if not wall_cols.empty else board.width - 1

            robot_cols = [c for r, c in other_robots_pos if r == self.row and c > self.col]
            robot_stop_col = min(robot_cols) if robot_cols else board.width

            final_robot_stop = robot_stop_col - 1 if robot_stop_col != board.width else board.width - 1
            self.col = min(wall_stop_col, final_robot_stop)

    def draw(
        self,
        screen: pygame.Surface,
        cell_width: int,
        cell_height: int,
        abs_x: int,
        abs_y: int,
    ) -> None:
        x = abs_x
        y = abs_y

        # Draw robot body (triangle)
        # Points for an isosceles triangle (base at bottom, apex pointing up)
        point1 = (x + cell_width // 2, y + cell_height // 3)  # Apex
        point2 = (x + cell_width // 3, y + 2 * cell_height // 3)  # Bottom-left
        point3 = (x + 2 * cell_width // 3, y + 2 * cell_height // 3)  # Bottom-right
        pygame.draw.polygon(screen, ROBOT_COLORS[self.color], [point1, point2, point3])
        pygame.draw.polygon(
            screen, (0, 0, 0), [point1, point2, point3], 2
        )  # Black border

        # Draw robot head (circle)
        head_x = x + cell_width // 2
        head_y = y + cell_height // 3
        pygame.draw.circle(
            screen, ROBOT_COLORS[self.color], (head_x, head_y), cell_width // 7
        )
        pygame.draw.circle(
            screen, (0, 0, 0), (head_x, head_y), cell_width // 7, 2
        )  # Black border
