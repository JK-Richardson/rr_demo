from src.common import (
    ROBOT_COLORS,
    TARGET_COLORS,
    TARGET_ROBOT_COLORS,
    TARGET_SHAPES,
    Direction,
    RobotColor,
    Target,
    TargetShape,
)


def test_direction_enum():
    assert Direction.UP.value == "UP"
    assert Direction.DOWN.value == "DOWN"
    assert Direction.LEFT.value == "LEFT"
    assert Direction.RIGHT.value == "RIGHT"


def test_robot_color_enum():
    assert RobotColor.RED.value == "RED"
    assert RobotColor.BLUE.value == "BLUE"
    assert RobotColor.GREEN.value == "GREEN"
    assert RobotColor.YELLOW.value == "YELLOW"


def test_target_enum():
    assert Target.RED_CIRCLE.value == "RED_CIRCLE"
    assert Target.BLUE_SQUARE.value == "BLUE_SQUARE"
    assert Target.GREEN_TRIANGLE.value == "GREEN_TRIANGLE"
    assert Target.YELLOW_ELLIPSE.value == "YELLOW_ELLIPSE"


def test_target_shape_enum():
    assert TargetShape.CIRCLE.value == "CIRCLE"
    assert TargetShape.SQUARE.value == "SQUARE"
    assert TargetShape.TRIANGLE.value == "TRIANGLE"
    assert TargetShape.ELLIPSE.value == "ELLIPSE"


def test_robot_colors_mapping():
    assert ROBOT_COLORS[RobotColor.RED] == (255, 0, 0)
    assert ROBOT_COLORS[RobotColor.BLUE] == (0, 0, 255)
    assert ROBOT_COLORS[RobotColor.GREEN] == (0, 255, 0)
    assert ROBOT_COLORS[RobotColor.YELLOW] == (255, 255, 0)


def test_target_shapes_mapping():
    assert TARGET_SHAPES[Target.RED_CIRCLE] == TargetShape.CIRCLE
    assert TARGET_SHAPES[Target.BLUE_SQUARE] == TargetShape.SQUARE
    assert TARGET_SHAPES[Target.GREEN_TRIANGLE] == TargetShape.TRIANGLE
    assert TARGET_SHAPES[Target.YELLOW_ELLIPSE] == TargetShape.ELLIPSE


def test_target_colors_mapping():
    assert TARGET_COLORS[Target.RED_CIRCLE] == (255, 0, 0)
    assert TARGET_COLORS[Target.BLUE_SQUARE] == (0, 0, 255)
    assert TARGET_COLORS[Target.GREEN_TRIANGLE] == (0, 255, 0)
    assert TARGET_COLORS[Target.YELLOW_ELLIPSE] == (255, 255, 0)


def test_target_robot_colors_mapping():
    assert TARGET_ROBOT_COLORS[Target.RED_CIRCLE] == RobotColor.RED
    assert TARGET_ROBOT_COLORS[Target.BLUE_SQUARE] == RobotColor.BLUE
    assert TARGET_ROBOT_COLORS[Target.GREEN_TRIANGLE] == RobotColor.GREEN
    assert TARGET_ROBOT_COLORS[Target.YELLOW_ELLIPSE] == RobotColor.YELLOW
