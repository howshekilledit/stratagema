import random
from utils import StackFrontier, QueueFrontier, Node
import time
import copy

# RULES
# 1. The board is a grid of cells
# 2. Each cell is colored magenta or cyan (m or c)
# 3. For each turn, the player can swap with an adjacent cell (up, down, left, right) or spread color to a diagonal cell (up-left, up-right, down-left, down-right).

class Board():
    def __init__(self, width = 2, height = 2, start = False):
        print('Creating board')

        # the board can be any size, but for most purposes, we'll use a 2x2 grid
        self.width = width
        self.height = height
        
        # color of each square is represented by 'm' or 'c' (magenta or cyan)
        # the player's position is represented by an uppercase letter (M or C)

        # if start is not provided, create a random grid
        if not start:
            self.grid = [[random.choice(['c', 'm'])  for _ in range(width)] for _ in range(height)]
            self.pos = intVector(random.randint(0, width-1), random.randint(0, height-1))
            self.char = self.getVal(self.pos)
            # if all letters are the same, change one to the opposite
            if len(set([cell for row in self.grid for cell in row])) == 1:
                x, y = self.pos.x, self.pos.y
                if self.grid[y][x] == 'm':
                    self.grid[y][x] = 'c'
                else:
                    self.grid[y][x] = 'm'
        else: # start, if provided, takes the form of a 2D list
            self.grid = copy.deepcopy(start)
            for y, row in enumerate(start):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        self.pos = intVector(x, y)
                        self.char = cell.lower()
                        self.grid[y][x] = cell.lower()
        self.goal = [[self.char] * self.width] * self.height #goal set 
        self.state = self.string_state() # current state      
   
    # returns a string grid representation of the current state, or of a given state
    def string_state(self, grid  = False, pos = False, console = False):
        if not grid:
            grid = self.grid
        if not pos:
            pos = self.pos
        printGrid = copy.deepcopy(grid) # copy the grid without reference
        printGrid = setVal(pos, self.char.upper(), printGrid)
        printGrid = '\n'.join([''.join(row) for row in printGrid])
        if console: # print to console if console is True
            print(printGrid)
        return printGrid

    # returns a grid from a string state representation
    def get_grid(self, state = False):
        if not state: # if no state is provided, use the current state
            state = self.state
        state = state.lower()
        return [list(row) for row in state.split('\n')]
    
    def terminal(self, grid = False):
        if not grid: # if no grid is provided, use the current grid
            grid = self.grid
        # check if all letters are the same
        return len(set([cell for row in grid for cell in row])) == 1
    
    def neighbors(self, pos = False):
        if not pos:
            pos = self.pos
        x, y = pos.x, pos.y
        neighbors = []
        # diagonal neighbors
        if x > 0 and y > 0:
            neighbors.append(intVector(x-1, y-1))
        if x < self.width - 1 and y > 0:
            neighbors.append(intVector(x+1, y-1))
        if x > 0 and y < self.height - 1:
            neighbors.append(intVector(x-1, y+1))
        if x < self.width - 1 and y < self.height - 1:
            neighbors.append(intVector(x+1, y+1))
        # horizontal  vertical neighbors
        if x > 0:
            neighbors.append(intVector(x-1, y))
        if x < self.width - 1:
            neighbors.append(intVector(x+1, y))
        if y > 0:
            neighbors.append(intVector(x, y-1))
        if y < self.height - 1:
            neighbors.append(intVector(x, y+1))
        return neighbors
    
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

    def moves(self, parent):
        pos = parent.action
        grid = self.get_grid(parent.state)
        moves = []
        for neighbor in self.neighbors(pos):
            if not is_diagonal(pos, neighbor):
            # swap places to the top, bottom, left, or right 
                neighborVal = self.getVal(neighbor, grid)
                playerVal = self.getVal(pos, grid)
                state = copy.deepcopy(grid)
                state = setVal(neighbor, playerVal, state)
                state = setVal(pos, neighborVal, state)
                action = neighbor # new position

            # TODO 3: add diagonal moves, which spraed the player's color to a diagonal cell

            # if state is set, create a new node
            if 'state' in locals():
                # if state is a list
                if isinstance(state, list):
                    state = self.string_state(state, action, False) # string representation of state
                # TODO 2: change below line to assign move to a Node instance with parent, state, and action
                move = None  
                moves.append(move)
        return moves
    
    def makeRandomMove(self, parent):
        moves = self.moves(parent)
        move = random.choice(moves)
        
        self.state = move.state
        self.pos = move.action
        self.grid = self.get_grid()
        return move

    def solve_random(self):
        parent = Node(state = self.state, action = self.pos, parent = None)
        self.string_state(console = True)
        self.print_break()
        while not self.terminal():
            parent = self.makeRandomMove(parent)
        self.record_solution(parent)

    def set_frontier(self, frontier): # set the frontier to be used for the search
        if frontier == 'stack':
            self.frontier = StackFrontier()
        elif frontier == 'queue':
            self.frontier = QueueFrontier()
        else:
            print('Invalid frontier. Use "stack" or "queue"')
        self.frontier.add(Node(state = self.state, action = self.pos, parent = None))
        self.explored = set()
        self.solution = False
    
    def print_break(self):
        print('-' * self.width)
    
    def record_solution(self, node): # record the solution path
        self.solution = []
        while node.parent is not None:
            self.solution.append(node)
            node = node.parent
        self.solution.reverse()
        for node in self.solution:
            print(node.state)
            self.print_break()
        print('Goal!')
    
    def solve_step(self): # solve one step at a time (type depends on the frontier)
        if self.frontier.empty():
            return None
        node = self.frontier.remove()
        self.removed = node.state
        if self.terminal(self.get_grid(node.state)):            
            self.record_solution(node)
            return
        self.explored.add(node.state)
        for move in self.moves(node):
            state = move.state
            pos = move.action
            if not self.frontier.contains_state(state) and state not in self.explored:
                child = Node(state=state, parent=node, action=pos)
                self.frontier.add(child)
    
    def solve(self):
        while not board.solution:
            board.solve_step()

def is_diagonal(pos1, pos2):
    # TODO 1: check if two positions, which are instances of the intVector class below, are diagonal
    # return True if they are diagonal, False otherwise
    raise NotImplementedError()


    

class intVector(): # vector class with integer coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y

def setVal(vec, val, grid): 
    x, y = vec.x, vec.y
    grid[y][x] = val
    return grid

if __name__ == '__main__':
    board = Board(2, 2, start = False)
    # print board
    board.string_state(console = True)
    # print break
    board.print_break()
    board.solve_random()

