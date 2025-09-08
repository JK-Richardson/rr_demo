# Ricochet Robots Game Plan

This document outlines the plan for creating the Ricochet Robots game.

## Game Concept

A faithful digital adaptation of the board game Ricochet Robots. Players try to find the shortest path for a robot to reach a target on a grid-based board. The robots move in straight lines and only stop when they hit a wall or another robot.

## Core Mechanics

*   Grid-based board with walls.
*   Multiple robots with different colors.
*   Robots move horizontally or vertically.
*   Robots continue moving until they hit an obstacle (wall or another robot).
*   A target chip on the board.
*   A designated robot must reach the target.
*   Players search for a sequence of moves to get the robot to the target.
*   Turn-based system for players to bid on the number of moves.
*   The player with the lowest bid gets to show their solution.

## MVP Features

*   A single, static game board.
*   Controllable robots that follow the movement rules.
*   A target that can be placed on the board.
*   A way to reset the robot positions.
*   A move counter.
*   A user interface to display the board, robots, and target.

## Asset List

*   **Graphics:**
    *   Board tiles (empty, wall)
    *   Robot sprites (different colors)
    *   Target chip sprite
*   **Sound:**
    *   Robot movement sound
    *   Collision sound (hitting a wall)
    *   Target reached sound

## Development Milestones

1.  **Milestone 1: Basic Board and Robot Movement**
    *   Create the game board grid.
    *   Implement robot movement logic.
    *   Render the board and a single robot.
    *   Allow the user to control the robot with keyboard input.

2.  **Milestone 2: Multiple Robots and Targets**
    *   Add multiple robots to the game.
    *   Implement collision between robots.
    *   Add a target to the board.
    *   Detect when the correct robot reaches the target.

3.  **Milestone 3: Game Loop and UI**
    *   Implement the main game loop (placing targets, resetting robots).
    *   Create a UI to display the current target, move count, and other game info.

4.  **Milestone 4: Bidding and Turn Structure**
    *   Implement the bidding system for players to guess the number of moves.
    *   Implement the turn structure for players to demonstrate their solutions.

5.  **Milestone 5: Polish and Refinements**
    *   Add sound effects.
    *   Improve graphics and animations.
    *   Add a main menu and settings screen.
