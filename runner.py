from stratagema import * 
import pyglet
from pyglet.gl import glClearColor
from pyglet import shapes
import random

# Board Config
CELL_SIZE = 50  # Adjust size to fit more grids on the screen
ROWS = 2
COLS = 2
MARGIN = 20  # Space between grids
MAX_COLS_PER_ROW = 5  # Maximum number of grids in a row before wrapping

# Colors
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)


class PygletBoard(Board):
    def __init__(self, width, height, start = False):
        super().__init__(width, height, start)
        self.window_width = (COLS * CELL_SIZE + MARGIN) * MAX_COLS_PER_ROW
        self.window_height = ROWS * CELL_SIZE + MARGIN
        self.window = pyglet.window.Window(self.window_width, self.window_height)
        self.batch = pyglet.graphics.Batch()
        self.grids = []
        self.player_circles = []  # To store circle representations of player positions
        self.create_grid(0, 0)

    def create_grid(self, x_offset, y_offset):
        grid_shapes = []
        for y in range(self.height):
            for x in range(self.width):
                color = MAGENTA if self.grid[y][x] == 'm' else CYAN
                rect = shapes.Rectangle(
                    x * CELL_SIZE + x_offset, y * CELL_SIZE + y_offset, CELL_SIZE, CELL_SIZE, color=color, batch=self.batch
                )
                grid_shapes.append(rect)
        self.grids.append(grid_shapes)

        # Draw the player as a circle at the current position
        player_x = self.pos.x * CELL_SIZE + CELL_SIZE // 2 + x_offset
        player_y = self.pos.y * CELL_SIZE + y_offset + CELL_SIZE // 2
        circle = shapes.Circle(player_x, player_y, CELL_SIZE // 4, color=WHITE, batch=self.batch)
        self.player_circles.append(circle)

    def move_player(self):
        parent = Node(state=self.state, action=self.pos, parent=None)
        self.makeRandomMove(parent)

        # Calculate new grid position based on the number of grids drawn
        num_grids = len(self.grids)
        row_index = num_grids // MAX_COLS_PER_ROW  # Row index
        col_index = num_grids % MAX_COLS_PER_ROW  # Column index within the row

        x_offset = col_index * (COLS * CELL_SIZE + MARGIN)
        y_offset = row_index * (ROWS * CELL_SIZE + MARGIN)  # Decrease y_offset to move down

        self.create_grid(x_offset, y_offset)

        # Resize window height if a new row is added
        new_window_height = (row_index + 1) * (ROWS * CELL_SIZE + MARGIN)
        self.window.set_size(self.window_width, new_window_height)

    def on_draw(self):
        glClearColor(0, 0, 0, 1)  # Clear the screen with black
        self.window.clear()
        self.batch.draw()

    def start(self):
        @self.window.event
        def on_draw():
            self.on_draw()

        def update(dt):
            if not self.terminal():
                self.move_player()

        pyglet.clock.schedule_interval(update, 1.0)  # Update every second
        pyglet.app.run()


if __name__ == "__main__":
    # Create a 2x2 board and visualize it using Pyglet
    pyglet_board = PygletBoard(ROWS, COLS)
    pyglet_board.start()

