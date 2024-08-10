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
                b = box(pos=vector(x*s+x_off, y*s+y_off, 1), size=vector(s, s, s), color=colors[cell.lower()])
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
    frontier_pos = vector(1, 10, 2) # position for next node in frontier
    text(pos=vector(9, 9, 1), text='frontier', height=0.5, color=color.black)
    b.set_frontier("queue", (frontier_pos.x, frontier_pos.y))
    # botton half, explored nodes
#    explored = box(pos=vector(0.5, -1, 0), size=vector(3, 1, 1), color=color.white)
#    text(pos=vector(0.5, -1, 0), text='explored', height=0.5, color=color.black)
    while not b.solution:
        rate(10)
        cycle_len = 70 # frames per cycle
        cycle_pos = f  % cycle_len # position in cycle
        if cycle_pos == 0: # start of cycle
            # remove node
            node = b.solve_step()
            ref = b.print(node.state, node.action, False)
            node_block = b.blocks[ref]
            # copy node block pos
            diff = frontier_pos - current_pos
            frontier_pos.x = len(b.frontier.frontier) * 4
        elif cycle_pos < 20:
            # move current node to current box
            for shape in b.blocks[ref]:
                shape.pos -= diff / 20
        # draw current node expansion in current section 
        elif cycle_pos == 20:
            # for each node in expanded node
            for i, n in enumerate(b.expanded):
                p = b.print(n.state, n.action, False)
                b.blocks[p] = b.draw(grid = p, origin = (current_pos.x + 3*i, current_pos.y - 3))
                if i == 0:
                    f_diff = frontier_pos - b.blocks[p][0].pos
        # pause after expanding node
        # then move node expansion blocks from current to frontier
        elif cycle_pos > 30 and cycle_pos < 50:
            # move blocks to frontier
            for i, n in enumerate(b.expanded):
                p = b.print(n.state, n.action, False)
                if b.blocks[p][0].pos.y > 0: # if not in explored
                    for shape in b.blocks[p]:
                        shape.pos += f_diff / 20
        elif cycle_pos >= 50 and cycle_pos < 70:
            # move current node to explored
           for shape in node_block:
               shape.pos.z = 1
               shape.pos.y -= 1
        #   
        #    # # draw node below board
        #   # #b.draw(grid = b.print(node.state, node.action, False), origin = (-10, y))
        #   # #b.drawFrontier()
        f += 1
