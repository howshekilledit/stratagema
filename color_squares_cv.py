import cv2
import numpy as np
from color_squares import *
import random

import cv2
import numpy as np

class BoardCV(Board):
    def __init__(self, width, height, cell_size = 10, start = False):
        super().__init__(width, height, start)
        self.cell_size = cell_size

    def draw(self, img = None, grid = None, s = None, origin = (0, 0)):
        if grid is None:
            grid = self.grid
            pos = self.pos
        if s is None:
            s = self.cell_size
        colors = {'r': (0, 0, 255), 'g': (0, 255, 0), 'b': (255, 0, 0), 'c': (255, 255, 0), 'm': (255, 0, 255), 'y': (0, 255, 255), 'w': (255, 255, 255), 'k': (0, 0, 0)}
        x_off, y_off = origin

        if isinstance(grid, str):
            grid = [[cell for cell in row] for row in grid.split('\n')]

            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        pos = (x, y)
        if img is None:
            img = np.zeros((len(grid)*s, len(grid[0])*s, 3), dtype=np.uint8)
        
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                cv2.rectangle(img, (x*s+x_off, y*s+y_off), ((x+1)*s+x_off, (y+1)*s+y_off), colors[cell.lower()], -1)
                if pos == (x, y):
                    cv2.circle(img, (x*s+s//2+x_off, y*s+s//2+y_off), s//3, (255, 255, 255), -1)

        #cv2.imshow('Board', img)
        #cv2.waitKey(1)
    def render_tree(self, file = 'output.png'):
        tree = board.group_tree()
        
        bw = board.width * board.cell_size # board width
        bh = board.height * board.cell_size # board height
        cs = board.cell_size # cell size
        width = 800
        height = 600
        # Create a blank image
        image = np.ones((height, width, 3), np.uint8) * 255

        pos_list = {}
        for y, tier in tree.items(): # for each distance group
            y = float(y) * 1.5
            tier_size = sum([len(group) for group in tier.values()]) + len(tier) -1 
            x_start = width/bw/2 - tier_size/2
            x = x_start
            for parent, group in tier.items(): #for each parent group
                if parent is not None:
                    
                    x = x
                    #x = max(((pos_list[parent][0]-x_start)/bw - len(group)/2), x) 
                else:
                    x = x_start
                for node in group:
                    grid = node.state
                    goal = False
                    if grid == board.goal:
                        goal = True
                    grid = board.print(grid, node.action, console = False)
                    px, py = int(x * bw), int(y * bh)
                    pos_list[grid] = (px, py)
                    if parent is not None:
                        ppos = pos_list[parent]
                        # draw line to parent
                        cv2.line(image, (ppos[0] + cs, ppos[1] + cs), (px + cs, py + cs), (0, 0, 0), 1)
                    # Display the grid
                    board.draw(image, grid, cs, (px, py))
                    #if goal:
                        #cv2.rectangle(image, (px, py), (px + bw, py + bh), (0, 0, 0), 2)
                    x += 1.1
                x += 1

        # Save the image
        cv2.imwrite(file, image)
if __name__ == '__main__':
    board = BoardCV(2, 2, 10)#, start = [['Y', 'y'], ['y', 'c']])
    board.print()
    board.decisionTree()
    board.render_tree('before_tree.png')
    board.duplicate_branches()
    board.render_tree('after_tree.png')
