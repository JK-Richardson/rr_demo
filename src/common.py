from enum import Enum

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class RobotColor(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"

ROBOT_COLORS = {
    RobotColor.RED: (255, 0, 0),
    RobotColor.BLUE: (0, 0, 255),
    RobotColor.GREEN: (0, 255, 0),
    RobotColor.YELLOW: (255, 255, 0),
}

class Target(Enum):
    RED_CIRCLE = "RED_CIRCLE"
    RED_SQUARE = "RED_SQUARE"
    RED_TRIANGLE = "RED_TRIANGLE"
    RED_ELLIPSE = "RED_ELLIPSE"

    BLUE_CIRCLE = "BLUE_CIRCLE"
    BLUE_SQUARE = "BLUE_SQUARE"
    BLUE_TRIANGLE = "BLUE_TRIANGLE"
    BLUE_ELLIPSE = "BLUE_ELLIPSE"

    GREEN_CIRCLE = "GREEN_CIRCLE"
    GREEN_SQUARE = "GREEN_SQUARE"
    GREEN_TRIANGLE = "GREEN_TRIANGLE"
    GREEN_ELLIPSE = "GREEN_ELLIPSE"

    YELLOW_CIRCLE = "YELLOW_CIRCLE"
    YELLOW_SQUARE = "YELLOW_SQUARE"
    YELLOW_TRIANGLE = "YELLOW_TRIANGLE"
    YELLOW_ELLIPSE = "YELLOW_ELLIPSE"

class TargetShape(Enum):
    CIRCLE = "CIRCLE"
    SQUARE = "SQUARE"
    TRIANGLE = "TRIANGLE"
    ELLIPSE = "ELLIPSE"

TARGET_SHAPES = {
    Target.RED_CIRCLE: TargetShape.CIRCLE,
    Target.RED_SQUARE: TargetShape.SQUARE,
    Target.RED_TRIANGLE: TargetShape.TRIANGLE,
    Target.RED_ELLIPSE: TargetShape.ELLIPSE,

    Target.BLUE_CIRCLE: TargetShape.CIRCLE,
    Target.BLUE_SQUARE: TargetShape.SQUARE,
    Target.BLUE_TRIANGLE: TargetShape.TRIANGLE,
    Target.BLUE_ELLIPSE: TargetShape.ELLIPSE,

    Target.GREEN_CIRCLE: TargetShape.CIRCLE,
    Target.GREEN_SQUARE: TargetShape.SQUARE,
    Target.GREEN_TRIANGLE: TargetShape.TRIANGLE,
    Target.GREEN_ELLIPSE: TargetShape.ELLIPSE,

    Target.YELLOW_CIRCLE: TargetShape.CIRCLE,
    Target.YELLOW_SQUARE: TargetShape.SQUARE,
    Target.YELLOW_TRIANGLE: TargetShape.TRIANGLE,
    Target.YELLOW_ELLIPSE: TargetShape.ELLIPSE,
}

TARGET_COLORS = {
    Target.RED_CIRCLE: (255, 0, 0),
    Target.RED_SQUARE: (255, 0, 0),
    Target.RED_TRIANGLE: (255, 0, 0),
    Target.RED_ELLIPSE: (255, 0, 0),

    Target.BLUE_CIRCLE: (0, 0, 255),
    Target.BLUE_SQUARE: (0, 0, 255),
    Target.BLUE_TRIANGLE: (0, 0, 255),
    Target.BLUE_ELLIPSE: (0, 0, 255),

    Target.GREEN_CIRCLE: (0, 255, 0),
    Target.GREEN_SQUARE: (0, 255, 0),
    Target.GREEN_TRIANGLE: (0, 255, 0),
    Target.GREEN_ELLIPSE: (0, 255, 0),

    Target.YELLOW_CIRCLE: (255, 255, 0),
    Target.YELLOW_SQUARE: (255, 255, 0),
    Target.YELLOW_TRIANGLE: (255, 255, 0),
    Target.YELLOW_ELLIPSE: (255, 255, 0),
}

TARGET_ROBOT_COLORS = {
    Target.RED_CIRCLE: RobotColor.RED,
    Target.RED_SQUARE: RobotColor.RED,
    Target.RED_TRIANGLE: RobotColor.RED,
    Target.RED_ELLIPSE: RobotColor.RED,

    Target.BLUE_CIRCLE: RobotColor.BLUE,
    Target.BLUE_SQUARE: RobotColor.BLUE,
    Target.BLUE_TRIANGLE: RobotColor.BLUE,
    Target.BLUE_ELLIPSE: RobotColor.BLUE,

    Target.GREEN_CIRCLE: RobotColor.GREEN,
    Target.GREEN_SQUARE: RobotColor.GREEN,
    Target.GREEN_TRIANGLE: RobotColor.GREEN,
    Target.GREEN_ELLIPSE: RobotColor.GREEN,

    Target.YELLOW_CIRCLE: RobotColor.YELLOW,
    Target.YELLOW_SQUARE: RobotColor.YELLOW,
    Target.YELLOW_TRIANGLE: RobotColor.YELLOW,
    Target.YELLOW_ELLIPSE: RobotColor.YELLOW,
}