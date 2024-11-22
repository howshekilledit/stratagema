from stratagema import *
from runner import * # comment this line out if not using runner


# Board Config

# TOOD  4 Update board to become too hard to solve randomly

CELL_SIZE = 50  # Adjust size to fit more grids on the screen
ROWS = 2
COLS = 2
MARGIN = 20  # Space between grids
MAX_COLS_PER_ROW = 5  # Maximum number of grids in a row before wrapping


# Colors
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)

if __name__ == "__main__":
    # Create a 2x2 board and visualize it using Pyglet
    pyglet_board = PygletBoard(ROWS, COLS)
    pyglet_board.start()
