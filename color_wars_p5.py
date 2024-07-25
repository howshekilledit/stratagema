from p5 import *
from color_wars import *

class BoardP5(Board):
        # display the board in p5
    def display(self):
        colors = {'r': Color(255, 0, 0), 'g': Color(0, 255, 0), 'b': Color(0, 0, 255)}
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                fill(colors[cell.lower()])
                rect((x * self.cell_size, y * self.cell_size), self.cell_size, self.cell_size)
                if self.pos.x == x and self.pos.y == y:
                    stroke(0)
                    rect((x * self.cell_size, y * self.cell_size), self.cell_size, self.cell_size)
                    ellipse((x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 2, self.cell_size // 2)
                    noStroke()
if __name__ == '__main__':
    board = BoardP5(2, 2, 100)
    board.print()
    def setup():
        size(board.width * board.cell_size, board.height * board.cell_size)
    def draw():
        background(255)
        board.display()
        if board.state == board.goal:
            print('You won!')
            text('You won!', 100, 100)
            noLoop()
        board.makeRandomMove()


    run(frame_rate=1)
