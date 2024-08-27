import pyglet
from pyglet.gl import glClearColor
from pyglet import shapes
import random
from stratagema import *


# Board Config
CELL_SIZE = 50  # Adjust size to fit more grids on the screen
ROWS = 2
COLS = 2
MARGIN = 20  # Space between grids

# Colors
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PygletBoard(Board):
    def __init__(self, width, height, start):
        super().__init__(width, height, start)
        self.window_height = WINDOW_HEIGHT = (ROWS * CELL_SIZE + MARGIN) * 1
        self.window_width = COLS * CELL_SIZE
        self.window = pyglet.window.Window(self.window_width, self.window_height)
        self.batch = pyglet.graphics.Batch()
        self.grids = []
        self.create_grid(0)

    def create_grid(self, y_offset):
        grid_shapes = []
        for y in range(self.height):
            for x in range(self.width):
                color = MAGENTA if self.grid[y][x] == 'm' else CYAN
                rect = shapes.Rectangle(
                    x * CELL_SIZE, y * CELL_SIZE + y_offset, CELL_SIZE, CELL_SIZE, color=color, batch=self.batch
                )
                grid_shapes.append(rect)
        self.grids.append(grid_shapes)

    def move_player(self):
        parent = Node(state=self.state, action=self.pos, parent=None)
        self.makeRandomMove(parent)
        # Calculate new y_offset based on the number of grids shown
        y_offset = (len(self.grids) * (ROWS * CELL_SIZE + MARGIN))
        self.create_grid(y_offset)
        # Resize window to fit the new grid
        self.window.set_size(self.window_width, y_offset + ROWS * CELL_SIZE + MARGIN)

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
    pyglet_board = PygletBoard(ROWS, COLS, start=[['m', 'C'], ['m', 'c']])
    pyglet_board.start()

