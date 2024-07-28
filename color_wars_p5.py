from p5 import *
from color_wars import *
import random

class BoardP5(Board): #extends color wars board for visualization in p5
    #add cell size argument to inherited __init__ method
    def __init__(self, width, height, cell_size = 10, start = False):
        super().__init__(width, height, start)
        self.cell_size = cell_size
    # display the board in p5
    def display(self, grid = None, s = None, origin = Vector(0, 0)):
        noStroke()
        pos = intVector(0, 0)
        if grid is None:
            grid = self.grid
            pos = self.pos
        if s is None:
            s = self.cell_size
        colors = {'r': Color(255, 0, 0), 'g': Color(0, 255, 0), 'b': Color(0, 0, 255), 'c': Color(0, 255, 255), 'm': Color(255, 0, 255), 'y': Color(255, 255, 0), 'w': Color(255), 'k': Color(0)}
        x_off, y_off = origin.x, origin.y
        # if grid is string
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
                    fill(0)
                    ellipse((x * s + s // 2 + x_off, y * s + s // 2 + y_off), s // 2, s // 2)

if __name__ == '__main__':
    board = BoardP5(2, 2, 10)#, start = [['Y', 'y'], ['y', 'c']])
    board.print()
    board.decisionTree()
    tree = board.group_tree()
    def setup():
        size(1200, 1200)
        background(255, 0, 0)
    def draw():
        background(255)
        bw = board.width * board.cell_size # board width
        bh = board.height * board.cell_size # board height
        cs = board.cell_size # cell size
        pos_list = {}
        for y, tier in tree.items(): # for each distance group
            y = float(y) * 1.5
            tier_size = sum([len(group) for group in tier.values()]) + len(tier) -1 
            x_start = width/bw/2 - tier_size/2
            x = x_start
            for parent, group in tier.items(): #for each parent group
                if parent is not None:
                    x = max(((pos_list[parent].x-x_start)/bw - len(group)/2), x) 
                else:
                    x = x_start
                for node in group:
                    grid = node.state
                    goal = False
                    if grid == board.goal:
                        goal = True
                    grid = board.print(grid, node.action, console = False)
                    px, py = x * bw, y * bh
                    pos_list[grid] = Vector(px, py)
                    if parent is not None:
                        ppos = pos_list[parent]
                        # draw line to parent
                        stroke(0)
                        try:
                            line((px + cs, py + cs), (ppos.x + cs, ppos.y + cs))
                        except:
                            print(pos_list)
                    board.display(grid, cs, Vector(px, py))
                    if goal:
                        stroke(0, 0, 0)
                        strokeWeight(2)
                        noFill()
                        rect(px, py, bw, bh)
                    x += 1.1
                x += 1
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
