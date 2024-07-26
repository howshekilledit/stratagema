import random
from utils import StackFrontier, QueueFrontier, Node
import time
import copy

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
        self.char = self.getVal(self.pos)
        self.goal = [[self.char] * self.width] * self.height #goal set <- change this line to TODO
        self.count()
    def count(self):
        count = 0
        val = self.getVal(self.pos).lower()
        for row in self.grid:
            for cell in row:
                if cell.lower() == val:
                    count += 1
    def print(self):
        printGrid = copy.deepcopy(self.grid) # copy the grid without reference
        printGrid = setVal(self.pos, self.char.upper(), printGrid)
        
        for row in printGrid:
            print(''.join(row))
    def neighbors(self, pos = False):
        if not pos:
            pos = self.pos
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
    def getVal(self, vec, grid = False):
        if not grid:
            grid = self.grid
        x, y = vec.x, vec.y
        return grid[y][x]
    def setVal(self, vec, val, inplace = True):
        x, y = vec.x, vec.y
        if inplace:
            self.grid[y][x] = val
        else: 
            return setVal(vec, val, self.grid)
    def moves(self, pos = False, grid = False):
        if not pos:
            pos = self.pos
        if not grid:
            grid = self.grid
        moves = []
        for neighbor in self.neighbors(pos):
            # spread colors to  neighbors to the diagonal
            if self.is_diagonal(pos, neighbor):
                # if color is not already the same  
                if self.getVal(neighbor, grid) != self.getVal(pos, grid):
                    state = copy.deepcopy(grid)
                    state = setVal(neighbor, self.getVal(pos, grid), state)
                    moves.append({'name': 'spread_color', 'newpos': pos, 'state': state})
            # swap places to the top, bottom, left, or right 
            else:
                neighborVal = self.getVal(neighbor, grid)
                agentVal = self.getVal(pos, grid)
                state = copy.deepcopy(grid)
                state = setVal(neighbor, agentVal, state)
                state = setVal(pos, neighborVal, state)
                moves.append({'name': 'swap_pos', 'newpos': neighbor, 'state': state})
        return moves
    def makeRandomMove(self):
        moves = self.moves()
        move = random.choice(moves)
        actionName = move[0]
        neighborPos = move[1]
        neighborVal = self.getVal(neighborPos)
        agentVal = self.getVal(self.pos)
        if actionName  == 'spread_color':
            self.setVal(neighborPos, agentVal)
        elif actionName  == 'swap_pos':
            self.setVal(neighborPos, agentVal)
            self.setVal(self.pos, neighborVal)
            self.pos = neighborPos
    def solve_random(self):
        while self.grid != self.goal:
            self.makeRandomMove()
            self.print()
            print('-'*self.width)
            #wait one second
            time.sleep(1)
        print('Goal!')
    def set_frontier(self, frontier_type):
        if frontier_type == 'stack':
            self.frontier = StackFrontier()
        elif frontier_type == 'queue':
            self.frontier = QueueFrontier()
        self.frontier.add(Node(self.grid, None, None))
        self.explored = set()
    def solve_bfs(self):
        self.set_frontier('queue')
        self.solve()
    def solve_dfs(self):
        self.set_frontier('stack')
        self.solve()
    def solve(self):
        while True:
            if self.frontier.empty():
                return None
            node = self.frontier.remove()
            print(node.state)
            if node.state == self.goal:
                print('Goal!')
                return
            self.explored.add(str(node.state))
            for move in self.moves(node.action, node.state):
                grid = move['state']
                pos = move['newpos']
                if not self.frontier.contains_state(grid)  and str(grid) not in self.explored:
                    child = Node(state=grid, parent=node, action=pos)
                    self.frontier.add(child)
if __name__ == '__main__':
    board = Board(2, 2, 100)
    board.print()
    board.solve_dfs()
