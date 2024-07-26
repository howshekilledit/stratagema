from p5 import *
from color_wars import *

class BoardP5(Board): #extends color wars board for visualization in p5
    #add cell size argument to inherited __init__ method
    def __init__(self, width, height, cell_size):
        super().__init__(width, height)
        self.cell_size = cell_size
        self.pos = intVector(0, 0)
    # display the board in p5
    def display(self, grid = None, s = None, origin = Vector(0, 0)):
        pos = intVector(0, 0)
        if grid is None:
            grid = self.grid
            pos = self.pos
        if s is None:
            s = self.cell_size
        colors = {'r': Color(255, 0, 0), 'g': Color(0, 255, 0), 'b': Color(0, 0, 255), 'c': Color(0, 255, 255), 'm': Color(255, 0, 255), 'y': Color(255, 255, 0), 'w': Color(255), 'k': Color(0)}
        x_off, y_off = origin.x, origin.y
        # if grid is string
        print(grid)
        if isinstance(grid, str):
            grid = [[cell for cell in row] for row in grid.split('\n')]
            
            # find the position of the player
            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        pos = intVector(x, y)
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                fill(colors[cell.lower()])
                rect((x * s + x_off, y * s + y_off), s, s)
                if pos.x == x and pos.y == y:
                    stroke(0)
                    rect((x * s + x_off, y * s + y_off), s, s)
                    ellipse((x * s + s // 2 + x_off, y * s + s // 2 + y_off), s // 2, s // 2)
                    noStroke()

if __name__ == '__main__':
    board = BoardP5(2, 2, 100)
    board.print()
    tree = board.decisionTree()
    def setup():
        size(1200, 1200)
        background(255, 0, 0)
        
    def draw():
        for y, tier in enumerate(tree):
            for x, grid in enumerate(tier):
                print(grid)
                board.display(grid, 10, Vector(x * 20, y * 20))
    #def setup():
    #    size(board.width * board.cell_size, board.height * board.cell_size)
    #    board.display()
    #    board.set_frontier('queue')
#    def draw():
#        background(255)
#        if board.grid == board.goal:
#            print('You won!')
#            text('You won!', 100, 100)
#            noLoop()
#        #board.solve_step()
#        board.makeRandomMove()
#        board.display(grid = board.removed)

    run(frame_rate=1)
