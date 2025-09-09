import pygame
import random

from board import Board
from robots import Robot, RobotColor, Direction, ROBOT_COLORS

class Game:
    def __init__(self):
        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800

        # Create the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Ricochet Robots")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Create the board
        self.board = Board()

        # Determine available starting positions for robots (not on targets)
        available_robot_start_coords = []
        for r in range(self.board.height):
            for c in range(self.board.width):
                if not self.board.grid[r][c].target:
                    available_robot_start_coords.append((r, c))
        random.shuffle(available_robot_start_coords)

        # Create robots and assign random starting positions
        robot_colors = [RobotColor.RED, RobotColor.BLUE, RobotColor.GREEN, RobotColor.YELLOW]
        self.robots = []
        for i, color in enumerate(robot_colors):
            if i < len(available_robot_start_coords):
                row, col = available_robot_start_coords[i]
                self.robots.append(Robot(color, row, col))
            else:
                # Handle case where there aren't enough unique spots for all robots
                print(f"Warning: Not enough unique starting positions for all robots. Robot {color.value} not placed.")

        self.selected_robot_index = 0

        # Game loop control
        self.running = True

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_robot_index = 0
                elif event.key == pygame.K_2:
                    self.selected_robot_index = 1
                elif event.key == pygame.K_3:
                    self.selected_robot_index = 2
                elif event.key == pygame.K_4:
                    self.selected_robot_index = 3
                
                selected_robot = self.robots[self.selected_robot_index]
                if event.key == pygame.K_UP:
                    selected_robot.move(Direction.UP, self.board, self.robots)
                elif event.key == pygame.K_DOWN:
                    selected_robot.move(Direction.DOWN, self.board, self.robots)
                elif event.key == pygame.K_LEFT:
                    selected_robot.move(Direction.LEFT, self.board, self.robots)
                elif event.key == pygame.K_RIGHT:
                    selected_robot.move(Direction.RIGHT, self.board, self.robots)

    def _update(self):
        # Game logic updates (e.g., check for win conditions, animations)
        pass

    def _draw(self):
        self.screen.fill(self.WHITE)

        self.board.draw(self.screen)

        cell_width = (self.SCREEN_WIDTH - 2 * self.board.buffer) // self.board.width
        cell_height = (self.SCREEN_HEIGHT - 2 * self.board.buffer) // self.board.height
        for i, robot_instance in enumerate(self.robots):
            robot_instance.draw(self.screen, cell_width, cell_height, self.board.buffer)
            if i == self.selected_robot_index:
                # Draw a highlight around the selected robot
                x = self.board.buffer + robot_instance.col * cell_width
                y = self.board.buffer + robot_instance.row * cell_height
                pygame.draw.rect(self.screen, (255, 255, 0), (x, y, cell_width, cell_height), 3) # Yellow border

        # Draw legend
        font = pygame.font.SysFont(None, 24)
        legend_x = 10
        legend_y = 10
        for i, robot_instance in enumerate(self.robots):
            text_color = ROBOT_COLORS[robot_instance.color]
            text_surface = font.render(f'{i+1}: {robot_instance.color.value}', True, text_color)
            self.screen.blit(text_surface, (legend_x, legend_y))
            legend_x += text_surface.get_width() + 20

        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_input()
            self._update()
            self._draw()
