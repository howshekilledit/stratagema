import random
from utils import StackFrontier, QueueFrontier, Node
import time
import copy

#RULES
#1. The board is a grid of cells
#2. Each cell is colored red, green, or blue
#3. For each turn, the player can swap with an adjacent cell (up, down, left, right) or spread color to a diagonal cell (up-left, up-right, down-left, down-right).
class intVector():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def setVal(vec, val, grid): # spec is a boolean that indicates if the update is speculative or not
    x, y = vec.x, vec.y
    grid[y][x] = val
    return grid

class Board():
    def __init__(self, width, height, start = False, branchDup = True):
        self.width = width
        self.height = height
        if not start:
            self.grid = [[random.choice(['c', 'm'])  for _ in range(width)] for _ in range(height)]
            self.pos = intVector(random.randint(0, width-1), random.randint(0, height-1))
        else:
            self.grid = start
            for y, row in enumerate(start):
                for x, cell in enumerate(row):
                    if cell.isupper():
                        self.pos = intVector(x, y)
                        self.char = cell.lower()
                        self.grid[y][x] = cell.lower()
        self.char = self.getVal(self.pos)
        self.goal = [[self.char] * self.width] * self.height #goal set <- change this line to TODO
        self.count()
        # enable or disable duplicate branches in decision tree (if enabled, all roads lead to goal)
        self.branchDup = branchDup
        if self.branchDup:
            self.branches = []
    def count(self):
        count = 0
        val = self.getVal(self.pos).lower()
        for row in self.grid:
            for cell in row:
                if cell.lower() == val:
                    count += 1
    def print(self, grid  = False, pos = False, console = True):
        if not grid:
            grid = self.grid
        if not pos:
            pos = self.pos
        printGrid = copy.deepcopy(grid) # copy the grid without reference
        printGrid = setVal(pos, self.char.upper(), printGrid)
        printGrid = '\n'.join([''.join(row) for row in printGrid])
        if console:
            print(printGrid)
        return printGrid
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
                    moves.append({'name': f"spread color", "affected_pos": neighbor, 'new_pos': pos, 'state': state})
            # swap places to the top, bottom, left, or right 
            else:
                neighborVal = self.getVal(neighbor, grid)
                playerVal = self.getVal(pos, grid)
                state = copy.deepcopy(grid)
                state = setVal(neighbor, playerVal, state)
                state = setVal(pos, neighborVal, state)
                moves.append({'name': "swap places", 'affected_pos': pos,  'new_pos': neighbor, 'state': state})
        return moves
    def makeRandomMove(self):
        moves = self.moves()
        move = random.choice(moves)
        self.grid = move['state']
        self.pos = move['new_pos']
    
    # create a decision tree
    def decisionTree(self, parent = None):
        if parent is None: # if parent is none, it's the first call
            self.tree = [] # create an empty tree
            parent = Node(state=self.grid, parent=parent, action=self.pos) # create a node for the current position
            self.tree.append(parent) # add the parent node to the tree
            self.explored = set() # set of explored grid
            self.explored.add(self.print(parent.state, parent.action, False)) # add the print output of the grid to the explored set
        moves = self.moves(parent.action, parent.state) # get the possible moves for the current position
        grids = [move['state'] for move in moves] # get the grids for each move
        for move in moves: # for each move
            grid = move['state'] # get the grid
            pos = move['new_pos']  # get the new position
            node = Node(state=grid, parent=parent, action=pos) # create a node for the move
            self.tree.append(node) # add the node to the tree
            pGrid = self.print(grid, pos, False) # get the print output for the grid
            if pGrid not in self.explored: # if the grid is not the goal and the print output is not in the explored set          
                self.explored.add(pGrid) # add the print output to the explored set
                if grid != self.goal:
                    self.decisionTree(node) # recursively call the decision tree with the new grid and moves
                elif self.branchDup: # if goal reached, record path
                    branch = [node]
                    while node.parent is not None:
                        node = node.parent
                        branch.append(node)
                    branch.reverse()
                    self.branches.append(branch)


    
    # add duplicate branches to the tree
    def duplicate_branches(self):
        # for each node in the decision tree that is not anyone's parent and is not the goal
        parents = set([node.parent for node in self.tree])
        for node in self.tree:
            if node not in parents and node.state != self.goal:
                # find branch that contains node with same state and action
                for branch in self.branches:
                    pgrids = [self.print(node.state, node.action, False) for node in branch]
                    p = self.print(node.state, node.action, False)
                    if p in pgrids:
                        parent = node
                        parents.add(parent)
                        # get index
                        index = pgrids.index(p)
                        for n in branch[index + 1:]:
                            dup_node = Node(state=n.state, parent=parent, action=n.action)
                            self.tree.append(dup_node)
                            parent = dup_node
                        break

    # group the tree by distance from the root node
    def group_tree(self):
        distances = []
        for node in self.tree:
            # get distance from root node
            distance = 0
            while node.parent is not None:
                distance += 1
                node = node.parent
            distances.append(distance)
        # group nodes by distance
        grouped = {}
        for i, distance in enumerate(distances):
            if distance not in grouped:
                grouped[distance] = set()
            grouped[distance].add(self.tree[i])
        # within each group, group by parent
        for distance in grouped:
            group = grouped[distance]
            parents = set([node.parent for node in group])
            grouped_group  = {}
            for parent in parents:
                if parent is None:
                    parent_name = None
                else:
                    parent_name = self.print(parent.state, parent.action, False)
                # Create a set to store the states of the nodes in the subgroup
                subgroup_states = set()
                for node in group:
                    if node.parent == parent:
                        # Check if the state of the node is already in the subgroup
                        p = self.print(node.state, node.action, False)
                        if p not in subgroup_states:
                            # If it's not, add the state to the set and the node to the subgroup
                            subgroup_states.add(p)
                            if parent_name not in grouped_group:
                                grouped_group[parent_name] = set()
                            grouped_group[parent_name].add(node)
                if len(grouped_group[parent_name]) > 3:
                    print(grouped_group[parent])
            grouped[distance] = grouped_group
        return grouped
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
        if frontier_type == 'queue':
            self.frontier = QueueFrontier()
        self.frontier.add(Node(self.grid, None, None))
        self.explored = set()
    def solve_bfs(self):
        self.set_frontier('queue')
        self.solve()
    def solve_dfs(self):
        self.set_frontier('stack')
        self.solve()
    def solve_step(self): # solve one step at a time (type depends on the frontier)
        if self.frontier.empty():
            return None
        node = self.frontier.remove()
        self.removed = node.state
        if node.state == self.goal:
            print('Goal!')
            return
        self.explored.add(str(node.state))
        for move in self.moves(node.action, node.state):
            grid = move['state']
            pos = move['new_pos']
            if not self.frontier.contains_state(grid)  and str(grid) not in self.explored:
                child = Node(state=grid, parent=node, action=pos)
                self.frontier.add(child)
    def solve(self):
        cost = 0
        while True:
            if self.frontier.empty():
                print('No solution')
                return None
            node = self.frontier.remove()
            self.removed = node.state
            if node.state == self.goal:
                self.solution = []
                while node.parent is not None:
                    self.solution.append(node)
                    node = node.parent
                self.solution.reverse()
                for node in self.solution:
                    self.print(node.state, node.action)
                    print('-'*self.width)
                print('Goal!')
                return
            self.explored.add(self.print(node.state, node.action, False))
            if node.action is not None:
                pos = node.action
            else:
                pos = self.pos
            for move in self.moves(pos, node.state):
                grid = move['state']
                pos = move['new_pos']
                if not self.frontier.contains_state(grid) and self.print(grid, pos, False) not in self.explored:
                    child = Node(state=grid, parent=node, action=pos)
                    self.frontier.add(child)
if __name__ == '__main__':
    board = Board(2, 2, start = [['B', 'b'], ['y', 'b']])
    board.print()
    print('-'*board.width)
    board.solve_bfs()
    #board.render_tree(board.decisionTree())
