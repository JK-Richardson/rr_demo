import sys
import os
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board import Board, Cell

@pytest.fixture
def board():
    """Returns a Board instance for testing."""
    return Board('tests/test_board.txt')

def test_board_dimensions(board):
    assert board.height == 3
    assert board.width == 3

def test_cell_walls(board):
    # Test cell (0, 0) - Should have North wall
    cell_0_0 = board.grid[0][0]
    assert cell_0_0.has_wall_north is True
    assert cell_0_0.has_wall_east is False
    assert cell_0_0.has_wall_south is False
    assert cell_0_0.has_wall_west is False

    # Test cell (0, 1) - Should have North and East walls
    cell_0_1 = board.grid[0][1]
    assert cell_0_1.has_wall_north is True
    assert cell_0_1.has_wall_east is True
    assert cell_0_1.has_wall_south is False
    assert cell_0_1.has_wall_west is False

    # Test cell (2, 2) - Should have no walls
    cell_2_2 = board.grid[2][2]
    assert cell_2_2.has_wall_north is False
    assert cell_2_2.has_wall_east is False
    assert cell_2_2.has_wall_south is False
    assert cell_2_2.has_wall_west is False