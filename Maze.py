import random as rand, pickle 
from Agent import Agent

class Maze():
    ## generate multiple shapes
    def __init__(self):
        self.features = dict({'empty':0,
                        'wall':1,
                        'honey':2,
                        'ice':3
        }) 

        self.locations = dict({'start':-1, 'goal':-2})
    def generate_random(self) -> list:
        """ Generate a maze with random size, start state and goal state """
        size = (rand.randint(20,100), rand.randint(20,100))
        start = (rand.randint(0, size[0]-1), rand.randint(0, size[1]-1))
        goal = (rand.randint(0, size[0]-1), rand.randint(0, size[1]-1))
        while goal == start:
            goal = (rand.randint(0, size[0]-1), rand.randint(0, size[1]-1))
        return self.generate(size, start, goal)

    def generate(self, size:tuple, start_state:tuple, goal_state:tuple) -> list:
        """ Generate a maze with given dimensions and start/goal states """
        maze = list()
        untouchables = dict({start_state:1, goal_state:1})
        for row in range(size[0]):
            column = list()
            for col in range(size[1]):
                if (row,col) == start_state:
                    column.append(self.locations['start'])
                elif (row,col) == goal_state:
                    column.append(self.locations['goal'])
                else:
                    column.append(rand.choice(list(self.features.values())))
            maze.append(column)

        while Agent.BFS(maze, start_state, goal_value=self.locations['goal'], wall_value=self.features['wall'])[0] == False:
            location1 = rand.randint(0,size[0]-1), rand.randint(0, size[1]-1)
            location2 = rand.randint(0,size[0]-1), rand.randint(0, size[1]-1)

            # It is still possible for l1 to = l2, due to later reassignment
            # The chancees were already low enough that I was questioning this next while loop anyhow
            while location1 == location2:
                location2 = rand.randint(0,size[0]-1), rand.randint(0, size[1]-1)

            while location1 in untouchables:
                location1 = rand.randint(0,size[0]-1), rand.randint(0, size[1]-1)

            while location2 in untouchables:
                location2 = rand.randint(0,size[0]-1), rand.randint(0, size[1]-1)

            maze[location1[0]][location1[1]], maze[location2[0]][location2[1]] = maze[location2[0]][location2[1]], maze[location1[0]][location1[1]]
        return maze


    def save(maze:list, filename:str) -> None:
        """ Not implemented """
        with open(filename, 'w') as f:
            for col in maze:
                pass

    def psave(maze:list, filename:str):
        """ Serialize with pickle. File must be *.p """
        with open(filename, 'wb') as fp:
            pickle.dump(filename, fp)
