from vpython import *
from color_squares import *
import sys

class Board3D(Board):
    def __init__(self, width, height, cell_size=1, start=False):
        super().__init__(width, height, start)
        self.cell_size = cell_size
        self.blocks = {}
    # extend set frontier
    def set_frontier(self, frontier, pos = (0, 0)):
        super().set_frontier(frontier)
        pgrid = self.print(console = False) 
        # add initial state to dictionary of blocks
        self.blocks[pgrid] = self.draw(grid = pgrid, origin = pos)
    def draw(self, grid=None, s=None, origin=(0, 0)):
        if grid is None:
            grid = self.grid
            pos = self.pos
        else:
            if isinstance(grid, str):
                grid = [[cell for cell in row] for row in grid.split('\n')]
            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        pos = (x, y)
        if s is None:
            s = self.cell_size
        colors = {'r': color.red, 'g': color.green, 'b': color.blue, 'c': color.cyan, 'm': color.magenta, 'y': color.yellow, 'w': color.white, 'k': color.black}
        x_off, y_off = origin
        shapes = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                b = box(pos=vector(x*s+x_off, y*s+y_off, 0), size=vector(s, s, s), color=colors[cell.lower()])
                shapes.append(b)
               # if pos == (x, y):
               #     # cut hole in b
            
               #     b.emissive = True
               #     b.opacity = 0.6
        return shapes
    def drawFrontier(self):
        for i, node in enumerate(self.frontier.frontier):
            p = self.print(node.state, node.action, False)
            


if __name__ == '__main__':
    b = Board3D(2, 2, start = [['m', 'C'], ['m', 'c']])
    y = 10

    f = 0 # frame counter

    # top left corner <- white box labeled "current"
    current = box(pos=vector(-10, 10, 0), size=vector(16, 8, 1), color=color.white)
    current_pos = vector(-10, 10, 2) # position for removed node
    text(pos=vector(-9, 9, 1), text='current', height=0.5, color=color.black)
    # top right corner <- white box labeled "frontier"
    frontier = box(pos=vector(10, 10, 0), size=vector(16, 8, 1), color=color.white)
    frontier_pos = vector(10, 10, 2) # position for next node in frontier
    text(pos=vector(9, 9, 1), text='frontier', height=0.5, color=color.black)
    b.set_frontier("queue", (10, 10))
    # botton half, explored nodes
#    explored = box(pos=vector(0.5, -1, 0), size=vector(3, 1, 1), color=color.white)
#    text(pos=vector(0.5, -1, 0), text='explored', height=0.5, color=color.black)
    while not b.solution:
        rate(10)
        cycle_pos = f % 60 # frames per cycle
        if cycle_pos == 0: # start of cycle
            # remove node
            node = b.solve_step()
            ref = b.print(node.state, node.action, False)
            diff = b.blocks[ref][0].pos - current_pos
        if cycle_pos < 20:
            # move block to current
            for shape in b.blocks[ref]:
                shape.pos -= diff / 20
        elif cycle_pos == 20:
           for i, n in enumerate(b.expanded):
                p = b.print(n.state, n.action, False)
                b.blocks[p] = b.draw(grid = p, origin = (-10 + 3 * i, 7))
        elif cycle_pos < 40:
            # move blocks to frontier
            for i, n in enumerate(b.expanded):
                p = b.print(n.state, n.action, False)
                if b.blocks[p][0].pos.y > 0: # if not in explored
                    for shape in b.blocks[p]:
                        shape.pos.z = 1
                        shape.pos.x += 1
        elif cycle_pos < 60:
            # move current node to explored
            for shape in b.blocks[ref]:
                shape.pos.z = 1
                shape.pos.y -= 1
           
            # # draw node below board
           # #b.draw(grid = b.print(node.state, node.action, False), origin = (-10, y))
           # #b.drawFrontier()
        f += 1
