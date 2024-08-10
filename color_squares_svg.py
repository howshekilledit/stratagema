import svgwrite
from color_squares import *
import random

class BoardSVG(Board):
    def __init__(self, width, height, cell_size=10, start=False):
        super().__init__(width, height, start)
        self.cell_size = cell_size

    def draw(self, dwg, grid=None, s=None, origin=(0, 0)):
        if grid is None:
            grid = self.grid
            pos = self.pos
        if s is None:
            s = self.cell_size
        colors = {'r': 'red', 'g': 'green', 'b': 'blue', 'c': 'cyan', 'm': 'magenta', 'y': 'yellow', 'w': 'white', 'k': 'black'}
        x_off, y_off = origin

        if isinstance(grid, str):
            grid = [[cell for cell in row] for row in grid.split('\n')]

            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        pos = (x, y)

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                dwg.add(dwg.rect(insert=(x*s+x_off, y*s+y_off), size=(s, s), fill=colors[cell.lower()]))
                if pos == (x, y):
                    dwg.add(dwg.circle(center=(x*s+s//2+x_off, y*s+s//2+y_off), r=s//3, fill='white'))

    def render_tree(self, file='output.svg'):
        tree = self.group_tree()

        bw = self.width * self.cell_size  # board width
        bh = self.height * self.cell_size  # board height
        cs = self.cell_size  # cell size
        width = 800
        height = 600
        
        # Create an SVG drawing
        dwg = svgwrite.Drawing(file, profile='tiny', size=(width, height))
        pos_list = {}

        for y, tier in tree.items():  # for each distance group
            y = float(y) * 1.5
            tier_size = sum([len(group) for group in tier.values()]) + len(tier) - 1
            x_start = width/bw/2 - tier_size/2
            x = x_start
            # order tier by x pos of parents
                           
            for parent, group in tier.items():  # for each parent group
                tier_xs = []
                if parent in pos_list:
                    if len(tier_xs) > 0:
                         x = max(max(tier_xs) + 1, pos_list[parent][0]/bw - 1)
                    else:
                         x = pos_list[parent][0]/bw - 1
                parent_positions = [pos_list[parent] for parent in tier.keys() if parent in pos_list]
                # order nodes by x pos of parents
                group = sorted(group, key=lambda node: parent_positions.index(pos_list[node.parent]) if node.parent in pos_list else 0)
                for node in group:
                    grid = node.state

                    goal = False
                    if grid == self.goal:
                        goal = True
                    grid = self.print(grid, node.action, console=False)
                    px, py = int(x * bw), int(y * bh)
                    pos_list[grid] = (px, py)
                    if parent is not None:
                        ppos = pos_list[parent]
                        # Draw a line to the parent
                        dwg.add(dwg.line(start=(ppos[0] + cs, ppos[1] + cs), end=(px + cs, py + cs), stroke='black'))

                    # Display the grid
                    self.draw(dwg, grid, cs, (px, py))
                    tier_xs.append(x)
                    x += 1.1
                x += 1

        # Save the SVG
        dwg.save()

if __name__ == '__main__':
    import sys
    lmt = sys.getrecursionlimit()
    print(lmt)
    sys.setrecursionlimit(1000000)
    board = BoardSVG(2, 2, 10)  # Initialize the board
    board.print()
    board.decisionTree()
    board.render_tree('all_paths_except_dup_states.svg')
    board.duplicate_branches()
    board.render_tree('dup_states_tree.svg')
    board.goal_tree()
    board.render_tree('limit_tree.svg')
    sys.setrecursionlimit(lmt)

