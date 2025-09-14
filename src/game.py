import logging
import pathlib
import random
import time  # Import time module

import pygame

from .board import Board, Cell, draw_target_shape  # Import Cell for type hinting
from .common import (  # Import Direction, RobotColor, Target, TARGET_SHAPES, ROBOT_COLORS, TARGET_ROBOT_COLORS, TARGET_COLORS from common.py
    ROBOT_COLORS,
    TARGET_COLORS,
    TARGET_ROBOT_COLORS,
    TARGET_SHAPES,
    Direction,
    RobotColor,
    Target,
)
from .robots import Robot


class Game:
    def __init__(self, config_path: pathlib.Path) -> None:
        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 1000  # Increased height for top and bottom gutters

        # Create the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("RR_DEMO")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Create the board
        self.board: Board = Board(config_path=config_path)

        # Determine available starting positions for robots (not on targets and not in the center)
        available_robot_start_coords: list[tuple[int, int]] = []
        reserved_cells = [(7, 7), (7, 8), (8, 7), (8, 8)]  # Central cells
        for r in range(self.board.height):
            for c in range(self.board.width):
                if not self.board.grid[r][c].target and (r, c) not in reserved_cells:
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
        self.initial_robot_positions: dict[RobotColor, tuple[int, int]] = {}
        for i, color in enumerate(robot_colors):
            if i < len(available_robot_start_coords):
                row, col = available_robot_start_coords[i]
                robot = Robot(color, row, col)
                self.robots.append(robot)
                self.initial_robot_positions[color] = (row, col)
            else:
                # Handle case where there aren't enough unique spots for all robots
                logging.warning(
                    f"Not enough unique starting positions for all robots. Robot {color.value} not placed."
                )

        self.selected_robot_index = 0

        # Select a random goal target
        self.goal_target = random.choice(list(Target))

        # Initialize move counter
        self.move_count = 0

        # Initialize game start time
        self.start_time = time.time()
        self.elapsed_time: float | None = None

        # Game loop control
        self.running = True

        # Pop-up message control
        self.show_popup = False
        self.popup_message = ""
        self.popup_move_count = 0

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_popup and self.ok_button_rect.collidepoint(event.pos):
                    self.show_popup = False  # Dismiss popup on OK button click
                    # TODO: Implement logic for new round after popup dismissal
                    return  # Consume the event
            elif event.type == pygame.KEYDOWN:
                if self.show_popup:
                    return  # Do not process key presses while popup is active

                if event.key == pygame.K_1:
                    self.selected_robot_index = 0
                elif event.key == pygame.K_2:
                    self.selected_robot_index = 1
                elif event.key == pygame.K_3:
                    self.selected_robot_index = 2
                elif event.key == pygame.K_4:
                    self.selected_robot_index = 3

                elif event.key == pygame.K_r:
                    # Reset board
                    for robot in self.robots:
                        initial_row, initial_col = self.initial_robot_positions[
                            robot.color
                        ]
                        robot.row = initial_row
                        robot.col = initial_col
                    self.move_count = 0

                selected_robot = self.robots[self.selected_robot_index]
                if event.key == pygame.K_UP:
                    selected_robot.move(Direction.UP, self.board, self.robots)
                    self.move_count += 1
                elif event.key == pygame.K_DOWN:
                    selected_robot.move(Direction.DOWN, self.board, self.robots)
                    self.move_count += 1
                elif event.key == pygame.K_LEFT:
                    selected_robot.move(Direction.LEFT, self.board, self.robots)
                    self.move_count += 1
                elif event.key == pygame.K_RIGHT:
                    selected_robot.move(Direction.RIGHT, self.board, self.robots)
                    self.move_count += 1

    def _update(self) -> None:
        # Check if the selected robot reached the goal target
        selected_robot = self.robots[self.selected_robot_index]

        found_goal_target_cell: Cell | None = None
        for r in range(self.board.height):
            for c in range(self.board.width):
                cell_target = self.board.grid[r][c].target
                if cell_target is not None and cell_target == self.goal_target:
                    found_goal_target_cell = self.board.grid[r][c]
                    break
            if found_goal_target_cell:
                break

        if found_goal_target_cell is None:
            logging.error(
                f"Goal target {self.goal_target.value} not found on the board."
            )
            return  # Exit update if goal target is not found

        # Now Pyright knows found_goal_target_cell is not None
        if (
            selected_robot.row == found_goal_target_cell.row
            and selected_robot.col == found_goal_target_cell.col
        ):
            # Check if the correct color robot reached the target
            required_robot_color = TARGET_ROBOT_COLORS.get(self.goal_target)
            if selected_robot.color == required_robot_color:
                if self.elapsed_time is None:  # Only set elapsed_time once
                    self.elapsed_time = time.time() - self.start_time
                logging.info(
                    f"Target {self.goal_target.value} reached by {selected_robot.color.value} robot!"
                )
                self.show_popup = True
                self.popup_move_count = self.move_count
                self.popup_message = f"Good job. You reached the target in {self.popup_move_count} moves in {self.elapsed_time:.2f} seconds."
                # TODO: Implement logic for new round (new target, reset robots, etc.)

    def _draw(self) -> None:
        self.screen.fill(self.WHITE)

        top_gutter_height = 100
        board_draw_height = (
            self.SCREEN_HEIGHT - top_gutter_height - 100
        )  # 100 pixels for bottom gutter

        self._draw_gutters(top_gutter_height, board_draw_height)
        self._draw_game_title(top_gutter_height)
        self._draw_legend(top_gutter_height)
        self._draw_board_area(board_draw_height, top_gutter_height)
        self._draw_robots(board_draw_height, top_gutter_height)
        self._draw_goal_target(top_gutter_height, board_draw_height)

        if self.show_popup:
            self._draw_popup()

        pygame.display.flip()

    def _draw_popup(self) -> None:
        # Draw a semi-transparent background
        overlay = pygame.Surface(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 128))  # Black with 128 alpha (half transparent)
        self.screen.blit(overlay, (0, 0))

        # Draw the message box
        box_width = 600
        box_height = 150
        box_x = (self.SCREEN_WIDTH - box_width) // 2
        box_y = (self.SCREEN_HEIGHT - box_height) // 2
        pygame.draw.rect(
            self.screen, self.WHITE, (box_x, box_y, box_width, box_height), 0, 10
        )  # White box with rounded corners
        pygame.draw.rect(
            self.screen, self.BLACK, (box_x, box_y, box_width, box_height), 3, 10
        )  # Black border

        # Draw the message text
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(self.popup_message, True, self.BLACK)
        text_rect = text_surface.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        )
        self.screen.blit(text_surface, text_rect)

        # Draw OK button
        button_width = 100
        button_height = 40
        button_x = (self.SCREEN_WIDTH - button_width) // 2
        button_y = (
            self.SCREEN_HEIGHT // 2 + box_height // 2 - button_height - 10
        )  # Position below text
        self.ok_button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height
        )
        pygame.draw.rect(
            self.screen, (0, 150, 0), self.ok_button_rect, 0, 5
        )  # Green button with rounded corners
        pygame.draw.rect(
            self.screen, self.BLACK, self.ok_button_rect, 2, 5
        )  # Black border

        button_font = pygame.font.SysFont(None, 30)
        button_text = button_font.render("OK", True, self.WHITE)
        button_text_rect = button_text.get_rect(center=self.ok_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def _draw_gutters(self, top_gutter_height: int, board_draw_height: int) -> None:
        # Draw top gutter
        pygame.draw.rect(
            self.screen, (200, 200, 200), (0, 0, self.SCREEN_WIDTH, top_gutter_height)
        )  # Grey top gutter background

        # Draw bottom gutter
        gutter_y = top_gutter_height + board_draw_height
        pygame.draw.rect(
            self.screen, (200, 200, 200), (0, gutter_y, self.SCREEN_WIDTH, 100)
        )  # Grey gutter background

    def _draw_game_title(self, top_gutter_height: int) -> None:
        # Draw Game Title in top gutter
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render("RR_DEMO", True, self.BLACK)
        title_rect = title_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, top_gutter_height // 3)
        )
        self.screen.blit(title_text, title_rect)

    def _draw_legend(self, top_gutter_height: int) -> None:
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

        # Draw move counter
        move_text = font.render(f"Moves: {self.move_count}", True, self.BLACK)
        self.screen.blit(
            move_text, (legend_x + 50, legend_y)
        )  # Position next to legend

    def _draw_board_area(self, board_draw_height: int, top_gutter_height: int) -> None:
        board_surface = pygame.Surface((self.SCREEN_WIDTH, board_draw_height))
        board_surface.fill(self.WHITE)
        self.board.draw(board_surface)
        self.screen.blit(board_surface, (0, top_gutter_height))

    def _draw_robots(self, board_draw_height: int, top_gutter_height: int) -> None:
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

    def _draw_goal_target(self, top_gutter_height: int, board_draw_height: int) -> None:
        gutter_y = top_gutter_height + board_draw_height
        font = pygame.font.SysFont(None, 24)
        # Draw Goal Target in gutter
        goal_text = font.render("Goal Target:", True, self.BLACK)
        self.screen.blit(goal_text, (10, gutter_y + 10))

        # Draw Reset instruction
        reset_text = font.render("R: reset", True, self.BLACK)
        self.screen.blit(
            reset_text, (self.SCREEN_WIDTH - reset_text.get_width() - 10, gutter_y + 10)
        )

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

    def run(self) -> None:
        while self.running:
            self._handle_input()
            self._update()
            self._draw()
