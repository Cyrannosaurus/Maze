import pickle

class Maze():
    def __init__(self, filename):
        # Read file
        with open(filename, 'r') as f:
            contents = f.read()
        
        if contents.count('A') != 1:
            raise Exception("Maze needs a single startpoint")
        if contents.count('B') != 1:
            raise Exception("Maze needs a single endpoint")

        contents = contents.splitlines()
        # Record height and width of maze
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Add context
        self.walls = [] # 2D bool array
        for r in range(self.height):
            row = []
            for c in range(self.width):
                # Try block as not all mazes will be rectangular
                try:
                    if contents[r][c] == '#':
                        row.append(True)
                    elif contents[r][c] == ' ':
                        row.append(False)
                    elif contents[r][c] == 'A':
                        self.start = (r,c)
                        row.append(False)
                    elif contents[r][c] == 'B':
                        self.goal = (r,c)
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(True)
            self.walls.append(row)
        self.solution = None

        self.horizontal_edges = set([0, self.height])
        self.vertical_edges = set([0, self.width])

        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for row in range(self.height):
            for col in range(self.width):
                if (row,col) == self.start:
                    print('A', end='')
                elif (row,col) == self.goal:
                    print('B', end='')
                elif self.walls[row][col] == True:
                    print('#', end='')
                elif solution is not None and (row,col) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()
        print()

        
    def neighbors(self, state):
        row, col = state
        # All possible actions
        candidates = [
            ('up', (row-1, col)),
            ('down', (row+1, col)),
            ('left', (row, col-1)),
            ('right', (row, col+1)),
        ]
        # Validate actions
        possible = []
        for action, (row, col) in candidates:
            try:
                if not self.walls[row][col]:
                    possible.append((action, (row,col)))
            except IndexError:
                continue
        return possible

    # Test which neighbor function is faster
    # def neighbors(self, state:Tuple[int,int]) -> list:
    #     neighbors = list()

    #     r = state[0]
    #     c = state[1]

    #     if r in self.horizontal_edges:
    #         if r == 0:
    #             neighbors.append((1, c))
    #         else:
    #             neighbors.append((self.height-1, c))
    #     else:
    #         neighbors.append((r-1, c))
    #         neighbors.append((r+1, c))

    #     if c in self.vertical_edges:
    #         if c == 0:
    #             neighbors.append((r, 1))
    #         else:
    #             neighbors.append((r, self.width-1))
    #     else:
    #         neighbors.append((r, c-1))
    #         neighbors.append((r, c+1))

    #     return neighbors

    def serialize(self, filename:str):
        """ Serialize with pickle. filename must be *.p """
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
