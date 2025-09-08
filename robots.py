from enum import Enum
import pygame

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

class Robot:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    def move(self, direction, board):
        if direction == Direction.UP:
            while self.row > 0 and not board.grid[self.row][self.col].has_wall_north and not board.grid[self.row - 1][self.col].has_wall_south:
                self.row -= 1
        elif direction == Direction.DOWN:
            while self.row < board.height - 1 and not board.grid[self.row][self.col].has_wall_south and not board.grid[self.row + 1][self.col].has_wall_north:
                self.row += 1
        elif direction == Direction.LEFT:
            while self.col > 0 and not board.grid[self.row][self.col].has_wall_west and not board.grid[self.row][self.col - 1].has_wall_east:
                self.col -= 1
        elif direction == Direction.RIGHT:
            while self.col < board.width - 1 and not board.grid[self.row][self.col].has_wall_east and not board.grid[self.row][self.col + 1].has_wall_west:
                self.col += 1

    def draw(self, screen, cell_width, cell_height, buffer):
        x = buffer + self.col * cell_width
        y = buffer + self.row * cell_height
        
        # Draw robot body (triangle)
        # Points for an isosceles triangle (base at bottom, apex pointing up)
        point1 = (x + cell_width // 2, y + cell_height // 3)  # Apex
        point2 = (x + cell_width // 3, y + 2 * cell_height // 3) # Bottom-left
        point3 = (x + 2 * cell_width // 3, y + 2 * cell_height // 3) # Bottom-right
        pygame.draw.polygon(screen, ROBOT_COLORS[self.color], [point1, point2, point3])

        # Draw robot head (circle)
        head_x = x + cell_width // 2
        head_y = y + cell_height // 3
        pygame.draw.circle(screen, ROBOT_COLORS[self.color], (head_x, head_y), cell_width // 7)