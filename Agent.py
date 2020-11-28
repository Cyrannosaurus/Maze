from Frontier import *

class Agent():
    def __init__(self):
        pass
    
    @staticmethod
    def BFS(maze:list, start_state:tuple, goal_value:int, wall_value:int):
        visited = set()
        frontier = QueueFrontier()
        frontier.add(Node(start_state, 0, None))
        while not frontier.empty():
            current = frontier.pop()
            visited.add(current.state)
            current_state = current.state
            if maze[current_state[0]][current_state[1]] == goal_value:
                path = list()
                while current != None:
                    path.append(current.state)
                    current = current.parent
                print(f'Visited a total of {len(visited)} unique nodes')
                path.reverse()
                return (True, path)
                
            neighbors = Agent.neighbors(current_state, maze)
            for neighbor in neighbors:
                if neighbor not in frontier.nodes and neighbor not in visited and maze[neighbor[0]][neighbor[1]] != wall_value:
                    frontier.add(Node(neighbor, None, current))
        return (False, None)



    @staticmethod
    def DFS(maze:list, start_state:tuple, goal_value:int, wall_value:int):
        visited = set()
        frontier = StackFrontier()
        frontier.add(Node(start_state, None, None))
        while not frontier.empty():
            current = frontier.pop()
            visited.add(current.state)
            current_state = current.state
            if maze[current_state[0]][current_state[1]] == goal_value:
                path = list()
                while current != None:
                    path.append(current.state)
                    current = current.parent
                path.reverse()
                return (True, path)
                
            neighbors = Agent.neighbors(current_state, maze)
            for neighbor in neighbors:
                if neighbor not in frontier.nodes and neighbor not in visited and maze[neighbor[0]][neighbor[1]] != wall_value:
                    frontier.add(Node(neighbor, None, current))

        return (False, None)

    def Beam(maze:list, start_state:tuple):
        pass

    @staticmethod
    def neighbors(state:tuple, maze:list) -> list:
        neighbors = list()
        max_r = len(maze) - 1
        max_c = len(maze[0]) - 1

        horizontal_edges = set([0, max_r])
        vertical_edges = set([0, max_c])

        r = state[0]
        c = state[1]

        if r in horizontal_edges:
            if r == 0:
                neighbors.append((1, c))
            else:
                neighbors.append((max_r-1, c))
        else:
            neighbors.append((r-1, c))
            neighbors.append((r+1, c))

        if c in vertical_edges:
            if c == 0:
                neighbors.append((r, 1))
            else:
                neighbors.append((r, max_c-1))
        else:
            neighbors.append((r, c-1))
            neighbors.append((r, c+1))

        return neighbors


