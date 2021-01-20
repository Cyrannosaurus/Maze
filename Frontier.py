import heapq
import sys
from collections import deque
from abc import ABC, abstractmethod
from typing import Deque, Iterable, List, Set, Tuple
# from functools import singledispatchmethod


class Node():
    """  A class for containing the data about a single position in a maze """
    def __init__(self, state:Tuple[int,int], cost:int, parent):
        self.state = state
        self.cost = cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state and self.cost == other.cost

    def worse_than(self,other):
        return self.state == other.state and self.cost > other.cost

    def __hash__(self):
        return (self.state,self.cost).__hash__()

    def __repr__(self) -> str:
        return f'{self.state}, {self.cost}'


class Frontier(ABC):
    """ The data structure that an agent will use to keep track of unexplored states """
    @abstractmethod
    def __init__(self):
        self.size : int = 0

    @abstractmethod
    def add(self, node: Node) -> None:
        pass

    @abstractmethod
    def pop(self) -> Node:
        pass

    @abstractmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        pass

    def is_empty(self):
        return self.size == 0

    @abstractmethod
    def __repr__(self):
        pass


class QueueFrontier(Frontier):
    """ A Queue based frontier no notion of cost """

    def __init__(self):
        super().__init__()
        self.nodes : Deque[Node] = deque()

    def add(self, node: Node) -> None:
        self.size += 1
        self.nodes.append(node)

    def pop(self) -> Node:
        self.size -= 1
        return self.nodes.popleft()

    # @singledispatchmethod
    # def contains(self, state):
    #     raise NotImplementedError("Cannot check for a")

    # @contains.register
    # def contains(self, state: Tuple[int,int]) -> bool:
    #     return any(node.state == state for node in self.nodes)
    
    # @contains.register
    def contains(self, node: Node) -> bool:
        return any(node == frontier_node for frontier_node in self.nodes)

    def __repr__(self):
        return self.nodes.__repr__()


class StackFrontier(Frontier):
    """ A Stack based frontier no notion of cost """

    def __init__(self):
        super().__init__()
        self.nodes : List[Node] = list()

    def add(self, node: Node) -> None:
        self.size += 1
        self.nodes.append(node)

    def pop(self) -> Node:
        self.size -= 1
        return self.nodes.pop(-1)

    # @singledispatchmethod
    # def contains(self, state):
    #     raise NotImplementedError("Cannot check for a")

    # @contains.register
    # def contains(self, state: Tuple[int,int]) -> bool:
    #     return any(node.state == state for node in self.nodes)
    
    # @contains.register
    def contains(self, node: Node) -> bool:
        return any(node == frontier_node for frontier_node in self.nodes)

    def __repr__(self):
        return self.nodes.__repr__()


class HeapFrontier(Frontier):
    """ A Heap based frontier utilizing a min-heap with a key of Node.cost """

    def __init__(self):
        super().__init__()
        self.nodes : List[Node] = list()
        self.marked : Set[int] = set()

    def add(self, node: Node) -> None:
        # add a node if there is not one with the same state and lower cost already in the heap
        code : int = self.perform_check(node)
        if code == -1:
            # A better or identical node exists in the heap already
            pass
        elif code == -2:
            # No node with this state exists in the heap
            heapq.heappush(self.nodes,node)
            self.size +=1
        else:
            # A worse node exists with the same state in the heap
            # We mark nodes to remove later as removing a node requires that we re-sort the heap, an expensive operation
            self.marked.add(hash(self.nodes[code]))
            heapq.heappush(self.nodes, node)
        return

    def pop(self) -> Node:
        node : Node = heapq.heappop(self.nodes)
        while hash(node) in self.marked:
            node = heapq.heappop(self.nodes)
        self.size -= 1
        return node


    # @singledispatchmethod
    # def contains(self, state):
    #     raise NotImplementedError("Cannot check for a")

    # @contains.register
    # def contains(self, state: Tuple[int,int]) -> bool:
    #     return any(node.state == state for node in self.nodes)
    
    # @contains.register
    def contains(self, node:Node) -> bool:
        return any(node.state == frontier_node.state and frontier_node.cost == node.cost for frontier_node in self.nodes)

    def perform_check(self, node: Node) -> int:
        """ 
        Return a code differntiating between three possible outcomes (from four scenarios):

                        Scenario                                        |   Outcome                                     |   Value
            - The given node has a new state                            |   Add new node                                |   -2
            - The given node has a seen state and (worse or equal) cost |   Do nothing                                  |   -1
            - The given node has a seen state and better cost           |   Add new node, mark existing for removal     |   index of node to remove
        """

        for i, known in enumerate(self.nodes):
            # Do nothing
            if known == node:
                return -1
            # Add new node and mark old one as skippable
            if known.worse_than(node):
                return i
            # Do nothing
            if node.worse_than(known):
                return -1
        # Add new node
        return -2

    def __repr__(self):
        rep : List[Tuple[int,int]] = list()
        for wrapper in self.nodes:
            rep.append(wrapper[0])
        return rep.__repr__()


class BeamFrontier():
    """ 
    A frontier for Beam Search
    Like QueueFrontier but only adds the best few predeccessor states from any given state as defined by 'width'
    """

    def __init__(self, width: int = sys.maxsize):
        self.size : int = 0 # A lower bound for the true size of self.nodes due to the lazy deletion of non-ideal nodes
        self.seen : int = 0
        self.nodes : List[Node] = list()
        self.marked : List[int] = list()
        self.width : int = width

    def update(self, neighbors: Iterable[Node]) -> None:
        " Adds the self.width lowest cost nodes from neighbors to the frontier "

        heapq.heapify(neighbors) # side-effect
        nodes : List[Node] = list()
        num_new_nodes = min(self.width,len(neighbors))
        i,j = 0,0

        # merge the now sorted lists
        # is it better to do the logic during the merging or after?

        # First way:
        # self.nodes = heapq.merge(self.nodes, neighbors[:self.width])
        # self.nodes = [node for i, node in enumerate(self.nodes) if not any(node.worse_than(node2) for node2 in self.nodes[i:])]

        # Second way:
        while i < self.size and (j < num_new_nodes):
            if self.nodes[i] < neighbors[j]:
                nodes.append(self.nodes[i])
                i+=1
            else:
                code = self.perform_check(neighbors[j])
                if code == -1:
                    # A better or identical node exists in the heap already
                    pass
                elif code == -2:
                    # No node with this state exists in the heap
                    nodes.append(self.nodes,neighbors[j])
                    self.size +=1
                else:
                    # A worse node exists with the same state in the heap
                    self.mark_worse(code)
                    nodes.append(self.nodes, neighbors[j])
                j+=1

        if i < self.size:
            nodes.extend(self.nodes[i:self.size])
        else:
            nodes.extend(neighbors[j:num_new_nodes])

        # Due to merging then removing repeat nodes, the first one can end up adding less nodes than defined by self.width even when there existed self.width valid nodes.

        self.nodes = nodes
        self.size += num_new_nodes


    def pop(self) -> Node:
        node : Node = heapq.heappop(self.nodes)
        while hash(node) in self.marked:
            node = heapq.heappop(self.nodes)
        self.size -= 1
        return node

    def mark_worse(self, index:int) -> None:
        " Add a node to the set of skippable nodes "
        # Done as removing a worse node requires that we re-sort the heap, an expensive operation
        self.marked.add(hash(self.nodes[index]))
        return 

    # @singledispatchmethod
    # def contains(self, state):
    #     raise NotImplementedError("Cannot check for a")

    # @contains.register
    # def contains(self, state: Tuple[int,int]) -> bool:
    #     return any(node.state == state for node in self.nodes)
    
    # @contains.register
    def contains(self, node:Node) -> bool:
        return any(node.state == frontier_node.state and frontier_node.cost == node.cost for frontier_node in self.nodes)

    def perform_check(self, node: Node) -> int:
        """ 
        Return a code differntiating between three possible outcomes (from four scenarios):

                        Scenario                                        |   Outcome                                     |   Value
            - The given node has a new state                            |   Add new node                                |   -2
            - The given node has a seen state and (worse or equal) cost |   Do nothing                                  |   -1
            - The given node has a seen state and better cost           |   Add new node, mark existing for removal     |   index of node to remove
        """

        for i, known in enumerate(self.nodes):
            # Do nothing
            if known == node:
                return -1
            # Add new node and mark old one as skippable
            if known.worse_than(node):
                return i
            # Do nothing
            if node.worse_than(known):
                return -1
        # Add new node
        return -2

    def __repr__(self):
        rep : List[Tuple[int,int]] = list()
        for wrapper in self.nodes:
            rep.append(wrapper[0])
        return rep.__repr__()
