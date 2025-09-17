import copy
from collections import deque
from typing import List, NamedTuple, Tuple, TypeAlias

from .common import Direction, RobotColor
from .game import Game
from .robots import Robot

# Move: (robot index, direction name)
Move: TypeAlias = Tuple[int, str]
Coord: TypeAlias = Tuple[int, int]


class State(NamedTuple):
    RED: Coord
    BLUE: Coord
    GREEN: Coord
    YELLOW: Coord


class Solution:
    def __init__(self, moves: List[Move] | None = None):
        self.moves = moves or []

    def __repr__(self):
        return f"Solution(moves={self.moves})"


class RobotContainer:
    def __init__(self, robots: List[Robot]) -> None:
        self.robots = robots
        self.robot_map = {robot.color: robot for robot in robots}
        self.red_robot = self.robot_map[RobotColor.RED]
        self.yellow_robot = self.robot_map[RobotColor.YELLOW]
        self.blue_robot = self.robot_map[RobotColor.BLUE]
        self.green_robot = self.robot_map[RobotColor.GREEN]

    def get_state(self) -> State:
        """Returns a State object with explicit members for each robot color"""
        return State(
            RED=self.red_robot.get_position(),
            BLUE=self.blue_robot.get_position(),
            GREEN=self.green_robot.get_position(),
            YELLOW=self.yellow_robot.get_position(),
        )

    def apply_state(self, state: State) -> None:
        """Sets the robots' positions according to the given State"""
        self.red_robot.row, self.red_robot.col = state.RED
        self.blue_robot.row, self.blue_robot.col = state.BLUE
        self.green_robot.row, self.green_robot.col = state.GREEN
        self.yellow_robot.row, self.yellow_robot.col = state.YELLOW


class Solver:
    def __init__(self, game: Game) -> None:
        self.visited = set()
        self.solution_path: list[Move] = []
        self.game = game
        _robots = copy.deepcopy(game.robots)
        self.robot_container = RobotContainer(_robots)

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
        robot_container = self.robot_container
        robots = robot_container.robots
        game = self.game
        initial_state = robot_container.get_state()
        self.visited: set[State] = set()
        self.queue: deque[tuple[State, list[Move]]] = deque([(initial_state, [])])
        self.queue.append((initial_state, []))  # (State, moves)
        self.visited.add(initial_state)
        solution = Solution()

        while self.queue:
            state, path = self.queue.popleft()
            robot_container.apply_state(state)

            if self.is_goal_state(game=self.game, robots=robots):
                self.solution_path = path
                solution = Solution(moves=path)
                break

            # For each robot, try each direction
            for robot_idx, robot in enumerate(robots):
                for direction in Direction:
                    # Move the robot
                    robot.move(direction, game.board, robots)
                    new_state = robot_container.get_state()
                    if new_state not in self.visited:
                        self.visited.add(new_state)
                        move_desc: Move = (robot_idx, direction.name)
                        self.queue.append((new_state, path + [move_desc]))
                    # Reset state for next iteration
                    robot_container.apply_state(state)

        return solution
