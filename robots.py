from enum import Enum
import pygame

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

class Robot:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    def draw(self, screen, cell_width, cell_height):
        x = self.col * cell_width + cell_width // 2
        y = self.row * cell_height + cell_height // 2
        pygame.draw.circle(screen, ROBOT_COLORS[self.color], (x, y), cell_width // 3)