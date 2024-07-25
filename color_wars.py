from p5 import *
import random

#RULES
#1. The board is a grid of cells
#2. Each cell is colored red, green, or blue
#3. For each turn, player can  change  neighbors to the top, bottom, left, and right to its color, as long as the color is not already the same. It can swap positions with neighbors to the diagonal, as long as the color is not already the same. It can swap colors with any neighbor whose color is different, including diagonal. 

class intVector():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def setVal(vec, val, grid): # spec is a boolean that indicates if the update is speculative or not
    x, y = vec.x, vec.y
    grid[y][x] = val
    return grid
class Board():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[random.choice(['r', 'g', 'b'])  for _ in range(width)] for _ in range(height)]
        self.pos = intVector(random.randint(0, width-1), random.randint(0, height-1))
        # get char at pos
        char = self.grid[int(self.pos.y)][int(self.pos.x)]
        # make char at pos uppercase
        self.grid[int(self.pos.y)][int(self.pos.x)] = char.upper()
        self.state = self.count()
    def count(self):
        count = 0
        val = self.getVal(self.pos).lower()
        for row in self.grid:
            for cell in row:
                if cell.lower() == val:
                    count += 1
        return
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
    # print the board in the console
    def print(self):
        for row in self.grid:
            print(''.join(row))
    def neighbors(self):
        x, y = self.pos.x, self.pos.y
        neighbors = []
        # horizontal  vertical neighbors
        if x > 0:
            neighbors.append(intVector(x-1, y))
        if x < self.width - 1:
            neighbors.append(intVector(x+1, y))
        if y > 0:
            neighbors.append(intVector(x, y-1))
        if y < self.height - 1:
            neighbors.append(intVector(x, y+1))
        # diagonal neighbors
        if x > 0 and y > 0:
            neighbors.append(intVector(x-1, y-1))
        if x < self.width - 1 and y > 0:
            neighbors.append(intVector(x+1, y-1))
        if x > 0 and y < self.height - 1:
            neighbors.append(intVector(x-1, y+1))
        if x < self.width - 1 and y < self.height - 1:
            neighbors.append(intVector(x+1, y+1))
        return neighbors
    def is_diagonal(self, pos1, pos2):
        return (abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)) == 2
    def getVal(self, vec):
        x, y = vec.x, vec.y
        return self.grid[y][x]
    def setVal(self, vec, val):
        x, y = vec.x, vec.y
        self.grid[y][x] = val
    def moves(self):
        moves = []
        for neighbor in self.neighbors():
            # spread colors to  neighbors to the diagonal
            if self.is_diagonal(self.pos, neighbor):
                # if color is not already the same  
                if self.getVal(neighbor).lower() != self.getVal(self.pos).lower():
                    moves.append(('spread_color', neighbor))
            # swap places to the top, bottom, left, or right 
            else:
                neighborVal = self.getVal(neighbor)
                agentVal = self.getVal(self.pos)
                moves.append(('swap_pos', neighbor))
            # swap colors with any neighbor whose color is different, including diagonal
            #moves.append(('swap_color', neighbor))
        return moves
    def makeRandomMove(self):
        moves = self.moves()
        move = random.choice(moves)
        actionName = move[0]
        neighborPos = move[1]
        neighborVal = self.getVal(neighborPos)
        agentVal = self.getVal(self.pos)
        if actionName  == 'spread_color':
            self.setVal(neighborPos, agentVal.lower())
        elif actionName  == 'swap_pos':
            self.setVal(neighborPos, agentVal)
            self.setVal(self.pos, neighborVal)
        elif actionName  == 'swap_color':
            self.setVal(neighborPos, agentVal.lower())
            self.setVal(self.pos, neighborVal.upper())
        # get index of pos in grid with uppercase letter
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.isupper():
                    self.pos = intVector(x, y)
                    break
        self.state = {'grid': self.grid, 'pos': self.pos}
    def update(self):
        pass

    def mouse_pressed(self):
        x = int(mouse_x // self.cell_size)
        y = int(mouse_y // self.cell_size)
        self.grid[y][x] = 255

if __name__ == '__main__':
    board = Board(5, 5, 20)
    board.print()
    def setup():
        size(board.width * board.cell_size, board.height * board.cell_size)
    def draw():
        background(255)
        board.display()
        board.print()
        board.makeRandomMove()
    def mouse_pressed():
        board.mouse_pressed()

    run(frame_rate=1)
