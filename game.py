import random

import pygame

from board import Board, draw_target_shape
from robots import Robot
from common import Direction, RobotColor, Target, TARGET_SHAPES, ROBOT_COLORS, TARGET_ROBOT_COLORS, TARGET_COLORS # Import Direction, RobotColor, Target, TARGET_SHAPES, ROBOT_COLORS, TARGET_ROBOT_COLORS, TARGET_COLORS from common.py


class Game:
    def __init__(self) -> None:
        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 1000  # Increased height for top and bottom gutters

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
        robot_colors = [
            RobotColor.RED,
            RobotColor.BLUE,
            RobotColor.GREEN,
            RobotColor.YELLOW,
        ]
        self.robots: list[Robot] = []
        for i, color in enumerate(robot_colors):
            if i < len(available_robot_start_coords):
                row, col = available_robot_start_coords[i]
                self.robots.append(Robot(color, row, col))
            else:
                # Handle case where there aren't enough unique spots for all robots
                print(
                    f"Warning: Not enough unique starting positions for all robots. Robot {color.value} not placed."
                )

        self.selected_robot_index = 0

        # Select a random goal target
        self.goal_target = random.choice(list(Target))

        # Game loop control
        self.running = True

    def _handle_input(self) -> None:
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

    def _update(self) -> None:
        # Check if the selected robot reached the goal target
        selected_robot = self.robots[self.selected_robot_index]
        goal_target_cell = None
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.grid[r][c].target == self.goal_target:
                    goal_target_cell = self.board.grid[r][c]
                    break
            if goal_target_cell:
                break

        if goal_target_cell and selected_robot.row == goal_target_cell.row and selected_robot.col == goal_target_cell.col:
            # Check if the correct color robot reached the target
            required_robot_color = TARGET_ROBOT_COLORS.get(self.goal_target)
            if selected_robot.color == required_robot_color:
                print(f"Target {self.goal_target.value} reached by {selected_robot.color.value} robot!")
                # TODO: Implement logic for new round (new target, reset robots, etc.)

    def _draw(self) -> None:
        self.screen.fill(self.WHITE)

        # Draw top gutter
        top_gutter_height = 100
        pygame.draw.rect(
            self.screen, (200, 200, 200), (0, 0, self.SCREEN_WIDTH, top_gutter_height)
        )  # Grey top gutter background

        # Calculate board drawing area (between top and bottom gutters)
        board_draw_height = (
            self.SCREEN_HEIGHT - top_gutter_height - 100
        )  # 100 pixels for bottom gutter

        # Draw Game Title in top gutter
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render("Ricochet Robots", True, self.BLACK)
        title_rect = title_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, top_gutter_height // 3)
        )
        self.screen.blit(title_text, title_rect)

        # Draw legend in top gutter
        font = pygame.font.SysFont(None, 24)
        legend_x = 10
        legend_y = top_gutter_height // 2 + 10  # Position below the title
        for i, robot_instance in enumerate(self.robots):
            text_color = ROBOT_COLORS[robot_instance.color]
            text_surface = font.render(
                f"{i + 1}: {robot_instance.color.value}", True, text_color
            )
            self.screen.blit(text_surface, (legend_x, legend_y))
            legend_x += text_surface.get_width() + 20

        board_surface = pygame.Surface((self.SCREEN_WIDTH, board_draw_height))
        board_surface.fill(self.WHITE)
        self.board.draw(board_surface)
        self.screen.blit(board_surface, (0, top_gutter_height))

        cell_width = (self.SCREEN_WIDTH - 2 * self.board.buffer) // self.board.width
        cell_height = (board_draw_height - 2 * self.board.buffer) // self.board.height
        for i, robot_instance in enumerate(self.robots):
            # Calculate absolute screen coordinates for the robot's cell
            abs_x = self.board.buffer + robot_instance.col * cell_width
            abs_y = (
                top_gutter_height + self.board.buffer + robot_instance.row * cell_height
            )
            robot_instance.draw(self.screen, cell_width, cell_height, abs_x, abs_y)
            if i == self.selected_robot_index:
                x = self.board.buffer + robot_instance.col * cell_width
                y = (
                    top_gutter_height
                    + self.board.buffer
                    + robot_instance.row * cell_height
                )  # Adjust y for top gutter
                pygame.draw.rect(
                    self.screen, (255, 255, 0), (x, y, cell_width, cell_height), 3
                )  # Yellow border

        # Draw bottom gutter
        gutter_y = top_gutter_height + board_draw_height
        pygame.draw.rect(
            self.screen, (200, 200, 200), (0, gutter_y, self.SCREEN_WIDTH, 100)
        )  # Grey gutter background

        # Draw Goal Target in gutter
        goal_text = font.render("Goal Target:", True, self.BLACK)
        self.screen.blit(goal_text, (10, gutter_y + 10))

        # Draw the goal target shape and color
        target_shape = TARGET_SHAPES.get(self.goal_target)
        target_color = TARGET_COLORS.get(self.goal_target)
        if target_shape and target_color:
            scaled_size = 40  # Example size
            target_center_x = 10 + goal_text.get_width() + 20 + scaled_size // 2
            target_center_y = gutter_y + 10 + goal_text.get_height() // 2

            # Use a scaled size for the target in the gutter
            draw_target_shape(
                self.screen,
                target_shape,
                target_color,
                target_center_x,
                target_center_y,
                scaled_size,
            )

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self._handle_input()
            self._update()
            self._draw()
