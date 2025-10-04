import pathlib

from src.common import Direction, RobotColor, Target
from src.game import Game
from src.solver import Solver


def test_solver_simple_one_move():
    """
    Tests a simple scenario where the solution is one move away.
    - The RED robot needs to reach the RED_CIRCLE target.
    - The board has a wall that will stop the robot exactly at the target.
    - Other robots are placed out of the way.
    """
    # Setup a deterministic game state
    # The RED robot is at (10, 2), the target is at (4, 2).
    # The cell at (4, 2) has a north wall, so moving UP from (10, 2)
    # will stop the robot at (4, 2).
    initial_positions = {
        RobotColor.RED: (10, 2),
        RobotColor.BLUE: (1, 1),
        RobotColor.GREEN: (1, 12),
        RobotColor.YELLOW: (12, 1),
    }
    # The RED_CIRCLE target is at (4, 2) according to board.yaml
    goal = Target.RED_CIRCLE

    game = Game(
        config_path=pathlib.Path("./board.yaml"),
        initial_robot_positions=initial_positions,
        goal_target=goal,
    )

    # The RED robot is the first robot in the list (index 0)
    # The expected move is (robot_index, direction)
    expected_solution = [(0, Direction.UP.name)]

    # Run the solver
    solver = Solver(game)
    solution = solver.solve()

    assert solution.moves == expected_solution