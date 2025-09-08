from board import Board

class BoardValidator:
    def __init__(self, board):
        self.board = board
        self.errors = []

    def validate(self):
        self.validate_perimeter_walls()
        self.validate_corner_walls()
        self.validate_no_four_walls()
        self.validate_neighbor_walls()
        return self.errors

    def validate_perimeter_walls(self):
        """Validates that all perimeter cells have an outer wall."""
        for r in range(self.board.height):
            if not self.board.grid[r][0].has_wall_west:
                self.errors.append(f"Cell ({r}, 0) is missing west wall.")
            if not self.board.grid[r][self.board.width - 1].has_wall_east:
                self.errors.append(f"Cell ({r}, {self.board.width - 1}) is missing east wall.")
        
        for c in range(self.board.width):
            if not self.board.grid[0][c].has_wall_north:
                self.errors.append(f"Cell (0, {c}) is missing north wall.")
            if not self.board.grid[self.board.height - 1][c].has_wall_south:
                self.errors.append(f"Cell ({self.board.height - 1}, {c}) is missing south wall.")

    def validate_corner_walls(self):
        """Validates that corner cells have both outer walls."""
        # Top-left
        if not (self.board.grid[0][0].has_wall_north and self.board.grid[0][0].has_wall_west):
            self.errors.append("Top-left corner is missing walls.")
        # Top-right
        if not (self.board.grid[0][self.board.width - 1].has_wall_north and self.board.grid[0][self.board.width - 1].has_wall_east):
            self.errors.append("Top-right corner is missing walls.")
        # Bottom-left
        if not (self.board.grid[self.board.height - 1][0].has_wall_south and self.board.grid[self.board.height - 1][0].has_wall_west):
            self.errors.append("Bottom-left corner is missing walls.")
        # Bottom-right
        if not (self.board.grid[self.board.height - 1][self.board.width - 1].has_wall_south and self.board.grid[self.board.height - 1][self.board.width - 1].has_wall_east):
            self.errors.append("Bottom-right corner is missing walls.")

    def validate_no_four_walls(self):
        """Validates that no cell has all four walls."""
        for r in range(self.board.height):
            for c in range(self.board.width):
                cell = self.board.grid[r][c]
                if cell.has_wall_north and cell.has_wall_east and cell.has_wall_south and cell.has_wall_west:
                    self.errors.append(f"Cell ({r}, {c}) has four walls.")

    def validate_neighbor_walls(self):
        """Validates that adjacent cells have consistent walls."""
        for r in range(self.board.height):
            for c in range(self.board.width):
                cell = self.board.grid[r][c]
                # Check neighbor to the south
                if r + 1 < self.board.height:
                    neighbor = self.board.grid[r + 1][c]
                    if cell.has_wall_south and neighbor.has_wall_north:
                        self.errors.append(f"Inconsistent south wall at ({r}, {c}) and north wall at ({r + 1}, {c}).")
                # Check neighbor to the east
                if c + 1 < self.board.width:
                    neighbor = self.board.grid[r][c + 1]
                    if cell.has_wall_east and neighbor.has_wall_west:
                        self.errors.append(f"Inconsistent east wall at ({r}, {c}) and west wall at ({r}, {c + 1}).")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python board_validator.py <path_to_board.txt>")
        sys.exit(1)
    
    board_file = sys.argv[1]
    try:
        board = Board(board_file)
        validator = BoardValidator(board)
        errors = validator.validate()
        if errors:
            print("Board validation failed with the following errors:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Board validation successful!")
    except FileNotFoundError:
        print(f"Error: Board file not found at '{board_file}'")
