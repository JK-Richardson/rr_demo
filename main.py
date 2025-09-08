import pygame

from board import Board
from robots import Robot, RobotColor, Direction, ROBOT_COLORS

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800  # Adjusted for a square board

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ricochet Robots")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the board
board = Board()

# Create robots
robots = [
    Robot(RobotColor.RED, 0, 0),
    Robot(RobotColor.BLUE, 5, 5)
]
selected_robot_index = 0

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_robot_index = 0
            elif event.key == pygame.K_2:
                selected_robot_index = 1
            
            selected_robot = robots[selected_robot_index]
            if event.key == pygame.K_UP:
                selected_robot.move(Direction.UP, board, robots)
            elif event.key == pygame.K_DOWN:
                selected_robot.move(Direction.DOWN, board, robots)
            elif event.key == pygame.K_LEFT:
                selected_robot.move(Direction.LEFT, board, robots)
            elif event.key == pygame.K_RIGHT:
                selected_robot.move(Direction.RIGHT, board, robots)

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the board
    board.draw(screen)

    # Draw robots
    cell_width = (SCREEN_WIDTH - 2 * board.buffer) // board.width
    cell_height = (SCREEN_HEIGHT - 2 * board.buffer) // board.height
    for i, robot_instance in enumerate(robots):
        robot_instance.draw(screen, cell_width, cell_height, board.buffer)
        if i == selected_robot_index:
            # Draw a highlight around the selected robot
            x = board.buffer + robot_instance.col * cell_width
            y = board.buffer + robot_instance.row * cell_height
            pygame.draw.rect(screen, (255, 255, 0), (x, y, cell_width, cell_height), 3) # Yellow border

    # Draw legend
    font = pygame.font.SysFont(None, 24)
    legend_x = 10 # Starting X position for legend
    legend_y = 10 # Y position for legend
    for i, robot_instance in enumerate(robots):
        text_color = ROBOT_COLORS[robot_instance.color]
        text_surface = font.render(f'{i+1}: {robot_instance.color.value}', True, text_color)
        screen.blit(text_surface, (legend_x, legend_y))
        legend_x += text_surface.get_width() + 20 # Move right for next legend item, with some padding

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
