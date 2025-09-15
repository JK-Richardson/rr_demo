import copy
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias

from .common import Direction, RobotColor
from .game import Game
from .robots import Robot

# Move: (robot index, direction name)
Move: TypeAlias = Tuple[int, str]
Coord: TypeAlias = Tuple[int, int]


@dataclass(frozen=True)
class State:
    RED: Coord
    BLUE: Coord
    GREEN: Coord
    YELLOW: Coord


class Solution:
    def __init__(self, moves: List[Move] | None = None):
        self.moves = moves or []

    def __repr__(self):
        return f"Solution(moves={self.moves})"


class Solver:
    def __init__(self, game: Game) -> None:
        self.visited = set()
        self.solution_path: list[Move] = []
        self.game = game
        self.initial_state = self.get_state(game.robots)

    def get_state(self, robots: list[Robot]) -> State:
        """Returns a State object with explicit members for each robot color"""
        robot_color_to_coords = {
            robot.color: (robot.row, robot.col) for robot in robots
        }
        return State(
            RED=robot_color_to_coords[RobotColor.RED],
            BLUE=robot_color_to_coords[RobotColor.BLUE],
            GREEN=robot_color_to_coords[RobotColor.GREEN],
            YELLOW=robot_color_to_coords[RobotColor.YELLOW],
        )

    def apply_state(self, state: State, robots: list[Robot]) -> None:
        """Sets the robots' positions according to the given State"""
        color_to_robot = {robot.color: robot for robot in robots}
        for color, pos in zip(
            [RobotColor.RED, RobotColor.BLUE, RobotColor.GREEN, RobotColor.YELLOW],
            [state.RED, state.BLUE, state.GREEN, state.YELLOW],
        ):
            if color in color_to_robot:
                robot = color_to_robot[color]
                robot.row, robot.col = pos

    def is_goal_state(self, game: Game, robots: list[Robot]) -> bool:
        """Checks if the target robot has reached the goal target"""
        target_robot_color = game.target_robot_color
        target_robot = next(
            robot for robot in robots if robot.color == target_robot_color
        )
        target_coords = game.target_cell_coords
        return (target_robot.row, target_robot.col) == target_coords

    def solve(self) -> Solution:
        """
        BFS to explore state space for Ricochet Robots.
        Returns a Solution object with the path to the goal (if found).
        """
        game = self.game
        robots = copy.deepcopy(game.robots)
        initial_state = self.get_state(robots)
        self.visited: set[State] = set()
        self.queue: deque[tuple[State, list[Move]]] = deque([(initial_state, [])])
        self.queue.append((initial_state, []))  # (State, moves)
        self.visited.add(initial_state)
        solution = Solution()

        while self.queue:
            state, path = self.queue.popleft()
            self.apply_state(state, robots)

            if self.is_goal_state(game=game, robots=robots):
                self.solution_path = path
                solution = Solution(moves=path)
                break

            # For each robot, try each direction
            for robot_idx, robot in enumerate(robots):
                for direction in Direction:
                    # Move the robot
                    robot.move(direction, game.board, robots)
                    new_state = self.get_state(robots)
                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        move_desc: Move = (robot_idx, direction.name)
                        self.queue.append((new_state, path + [move_desc]))
                    # Reset state for next iteration
                    self.apply_state(state, robots)

        return solution
