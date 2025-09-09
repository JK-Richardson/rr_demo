import pygame
import yaml
import random
from targets import Target, TARGET_COLORS, TargetShape, TARGET_SHAPES

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.has_wall_north = False
        self.has_wall_east = False
        self.has_wall_south = False
        self.has_wall_west = False
        self.target = None

class Board:
    def __init__(self, config_path='board.yaml'):
        config = self._load_config(config_path)
        self.width = config['width']
        self.height = config['height']
        self.grid = self._create_empty_grid(self.width, self.height)

        self.grid_line_color = tuple(config.get('grid_line_color', [200, 200, 200]))
        self.wall_color = tuple(config.get('wall_color', [255, 0, 0]))
        self.show_cell_coords = config.get('show_cell_coords', False)

        self.font = pygame.font.SysFont(None, 24)
        self.target_font = pygame.font.SysFont("dejavusans", 32)
        self.buffer = 50
        
        # Randomly assign target coordinates
        available_coords = [tuple(coord) for coord in config['target_coordinates']]
        random.shuffle(available_coords)

        all_targets = list(Target) # Get all target enums
        if len(available_coords) < len(all_targets):
            raise ValueError("Not enough unique coordinates for all targets.")

        for i, target_enum in enumerate(all_targets):
            row, col = available_coords[i]
            self.grid[row][col].target = target_enum

        self._apply_walls(config)

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def _apply_walls(self, config):
        # Apply outer border walls
        for r in range(self.height):
            self.grid[r][0].has_wall_west = True
            self.grid[r][self.width - 1].has_wall_east = True
        for c in range(self.width):
            self.grid[0][c].has_wall_north = True
            self.grid[self.height - 1][c].has_wall_south = True

        # Apply internal walls from config
        walls_config = config['walls']
        for coord_str, wall_def in walls_config.items():
            # Convert string key "(row, col)" to tuple (row, col)
            row, col = map(int, coord_str.strip('()').split(','))
            cell = self.grid[row][col]
            if 'N' in wall_def:
                cell.has_wall_north = True
            if 'E' in wall_def:
                cell.has_wall_east = True
            if 'S' in wall_def:
                cell.has_wall_south = True
            if 'W' in wall_def:
                cell.has_wall_west = True

    def _create_empty_grid(self, width, height):
        grid = []
        for r in range(height):
            row = []
            for c in range(width):
                cell = Cell(r, c)
                row.append(cell)
            grid.append(row)
        return grid

    def draw(self, screen):
        cell_width = (screen.get_width() - 2 * self.buffer) // self.width
        cell_height = (screen.get_height() - 2 * self.buffer) // self.height

        # Draw grid lines
        for r in range(self.height):
            for c in range(self.width):
                x = self.buffer + c * cell_width
                y = self.buffer + r * cell_height
                # Draw horizontal grid line
                pygame.draw.line(screen, self.grid_line_color, (x, y), (x + cell_width, y), 1)
                # Draw vertical grid line
                pygame.draw.line(screen, self.grid_line_color, (x, y), (x, y + cell_height), 1)

        # Draw walls and targets
        for r in range(self.height):
            for c in range(self.width):
                cell = self.grid[r][c]
                x = self.buffer + c * cell_width
                y = self.buffer + r * cell_height

                if cell.has_wall_north:
                    pygame.draw.line(screen, self.wall_color, (x, y), (x + cell_width, y), 4)
                if cell.has_wall_east:
                    pygame.draw.line(screen, self.wall_color, (x + cell_width, y), (x + cell_width, y + cell_height), 4)
                if cell.has_wall_south:
                    pygame.draw.line(screen, self.wall_color, (x, y + cell_height), (x + cell_width, y + cell_height), 4)
                if cell.has_wall_west:
                    pygame.draw.line(screen, self.wall_color, (x, y), (x, y + cell_height), 4)
                
                if cell.target:
                    shape = TARGET_SHAPES.get(cell.target)
                    color = TARGET_COLORS.get(cell.target)
                    if shape and color:
                        center_x = x + cell_width // 2
                        center_y = y + cell_height // 2
                        
                        if shape == TargetShape.CIRCLE:
                            pygame.draw.circle(screen, color, (center_x, center_y), cell_width // 3)
                        elif shape == TargetShape.SQUARE:
                            side = cell_width // 1.5
                            square_rect = pygame.Rect(center_x - side // 2, center_y - side // 2, side, side)
                            pygame.draw.rect(screen, color, square_rect)
                        elif shape == TargetShape.TRIANGLE:
                            # Points for an equilateral triangle pointing up
                            point1 = (center_x, center_y - cell_height // 3)
                            point2 = (center_x - cell_width // 3, center_y + cell_height // 3)
                            point3 = (center_x + cell_width // 3, center_y + cell_height // 3)
                            pygame.draw.polygon(screen, color, [point1, point2, point3])
                        elif shape == TargetShape.ELLIPSE:
                            ellipse_rect = pygame.Rect(center_x - cell_width // 3, center_y - cell_height // 4, 2 * cell_width // 3, 2 * cell_height // 4)
                            pygame.draw.ellipse(screen, color, ellipse_rect)

                if self.show_cell_coords:
                    text = self.font.render(f'{r},{c}', True, (0,0,0))
                    screen.blit(text, (x + 5, y + 5))
