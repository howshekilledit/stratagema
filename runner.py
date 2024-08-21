import pyglet
from pyglet.window import key
from pyglet.gl import glClearColor
from pyglet import shapes
from random import choice
from color_squares import *
import random

# Board Config
CELL_SIZE = 100
ROWS = 2
COLS = 2
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Colors
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PygletBoard(Board):
    def __init__(self, width, height, start):
        super().__init__(width, height, start)
        self.window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.batch = pyglet.graphics.Batch()
        self.shapes = []
        self.create_grid()

    def create_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                color = MAGENTA if self.grid[y][x] == 'm' else CYAN
                rect = shapes.Rectangle(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, color=color, batch=self.batch)
                self.shapes.append(rect)
                # draw a circle over self.pos
        x, y = self.pos.x, self.pos.y
        circle = shapes.Circle(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 4, color=WHITE, batch=self.batch)
        self.shapes.append(circle)

    def update_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                idx = y * self.width + x
                color = MAGENTA if self.grid[y][x] == 'm' else CYAN
                self.shapes[idx].color = color
        # update circle position
        x, y = self.pos.x, self.pos.y
        self.shapes[-1].x = x * CELL_SIZE + CELL_SIZE // 2

    def draw(self):
        glClearColor(0, 0, 0, 1)  # Clear the screen with black
        self.window.clear()
        self.batch.draw()

    def on_draw(self):
        self.window.clear()
        self.draw()

    def move_player(self):
        parent = Node(state=self.state, action=self.pos, parent=None)
        self.makeRandomMove(parent)
        self.update_grid()

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

