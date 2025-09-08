import pygame
import yaml
from targets import Target, TARGET_SYMBOLS, TARGET_COLORS

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
    def __init__(self, file_path, config_path='board.yaml'):
        self.grid = self._load_board_from_file(file_path)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self._load_config_and_place_targets(config_path)
        self.font = pygame.font.SysFont(None, 24)
        self.target_font = pygame.font.SysFont("dejavusans", 32)
        self.buffer = 50

    def _load_config_and_place_targets(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.grid_line_color = tuple(config.get('grid_line_color', [200, 200, 200]))
        self.wall_color = tuple(config.get('wall_color', [255, 0, 0]))
        self.show_cell_coords = config.get('show_cell_coords', False)
        
        targets = config.get('targets', {})
        for target_id, pos in targets.items():
            try:
                target = Target(target_id)
                row, col = pos
                self.grid[row][col].target = target
            except (ValueError, IndexError):
                # Handle invalid target definition or position
                pass

    def _load_board_from_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        grid = []
        # Skip header row
        for r, line in enumerate(lines[1:]):
            row = []
            # Skip row label
            cells = [c.strip() for c in line.strip().split(',')[1:]]
            for c, wall_def in enumerate(cells):
                cell = Cell(r, c)
                if 'N' in wall_def:
                    cell.has_wall_north = True
                if 'E' in wall_def:
                    cell.has_wall_east = True
                if 'S' in wall_def:
                    cell.has_wall_south = True
                if 'W' in wall_def:
                    cell.has_wall_west = True
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
                    symbol = TARGET_SYMBOLS.get(cell.target)
                    color = TARGET_COLORS.get(cell.target)
                    if symbol and color:
                        text = self.target_font.render(symbol, True, color)
                        text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                        screen.blit(text, text_rect)

                if self.show_cell_coords:
                    text = self.font.render(f'{r},{c}', True, (0,0,0))
                    screen.blit(text, (x + 5, y + 5))
