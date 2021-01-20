from Frontier import *
from Maze import Maze



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
            if not frontier.contains(neighbor) and neighbor not in visited:
                frontier.add(Node(neighbor, None, current))
    return (False, None)



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


