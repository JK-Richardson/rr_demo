import pygame
from board import Board

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800 # Adjusted for a square board

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ricochet Robots")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the board
board = Board('board.txt')

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the board
    board.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
