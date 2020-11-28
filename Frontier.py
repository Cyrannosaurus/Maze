import heapq
import sys
from collections import deque
from abc import ABC, abstractmethod
from typing import Deque, Iterable, List, Set, Tuple
from functools import singledispatchmethod
from dataclasses import dataclass


class Node(dataclass):
    """  A class for containing the data about a single position in the game """
    state: Tuple[int,int]
    cost: int

    def __lt__(self, other):
        return self.cost < other.cost


class Frontier(ABC):
    """ The data structure that an agent will use to keep track of unexplored states """
    @abstractmethod
    def __init__(self):
        self.size : int = 0
        self.seen : int = 0

    @abstractmethod
    def add(self, node: Node) -> None:
        pass

    @abstractmethod
    def pop(self) -> Node:
        pass

    @abstractmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        pass

    def empty(self):
        return self.size == 0

    @abstractmethod
    def __repr__(self):
        pass


class QueueFrontier(Frontier):
    """ A frontier for Breadth First Search with no notion of cost """

    def __init__(self):
        super().__init__()
        self.nodes : Deque[Node] = deque()

    def add(self, node: Node) -> None:
        self.size += 1
        self.nodes.append(node)

    def pop(self) -> Node:
        self.size -= 1
        return self.nodes.popleft()

    @singledispatchmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        return any(node.state == state for node in self.nodes)
    
    @contains.register(Node)
    def contains(self, node: Node) -> bool:
        return any(node.state == frontier_node.state for frontier_node in self.nodes)

    def __repr__(self):
        return self.nodes.__repr__()


class StackFrontier(Frontier):
    """ A frontier for Depth First Search with no notion of cost """

    def __init__(self):
        super().__init__()
        self.nodes : List[Node] = list()

    def add(self, node: Node) -> None:
        self.size += 1
        self.nodes.append(node)

    def pop(self) -> Node:
        self.size -= 1
        return self.nodes.pop(-1)

    @singledispatchmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        return any(node.state == state for node in self.nodes)
    
    @contains.register(Node)
    def contains(self, node: Node) -> bool:
        return any(node.state == frontier_node.state for frontier_node in self.nodes)

    def __repr__(self):
        return self.nodes.__repr__()


class HeapFrontier(Frontier):
    def __init__(self, max_size : int = sys.maxint):
        super().__init__()
        self.nodes : List[Node] = list()
        self.max_size : int = max_size
        self.marked : Set[Node] = set()

    def add(self, node: Node) -> None:
        if not self.contains(node.state):
            self.seen += 1
            # Use the current size of the frontier as a tie-breaker
            # We are prioritizing earlier paths than later ones
            heapq.heappush(self.nodes, node)
            self.size += 1
        else:
            if self._contains_lt(node):
                self.nodes.pop(self._index_lt(node))
                heapq.heapify(self.nodes)
                heapq.heappush(self.nodes, node)
        return

    def pop(self) -> Node:
        ret = heapq.heappop(self.nodes)
        while ret in self.marked:
            ret = heapq.heappop(self.nodes)
        self.size -= 1
        return ret[-1]

    def remove(self, node: Node) -> None:
        return self.nodes.remove(node)

    """ Returns the index of a node with same state and less cost than the given. Returns negative one if not found. """
    def _index_lt(self, node:Node) -> int:
        for i, known in enumerate(self.nodes):
            if node.state == known.state and known.cost < node.cost:
                return i
        return -1

    @singledispatchmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        return any(node.state == state for node in self.nodes)
    
    @contains.register(Node)
    def contains(self, node: Node) -> bool:
        return any(node.state == frontier_node.state for frontier_node in self.nodes)

    """ Returns true if a node exists in the frontier with the same state but lower cost then the given """
    def _contains_lt(self, node:Node) -> bool:
        # Should we prioritize older states or recent states when a state is refound with the same cost?
        return any(node.state == known.state and known.cost < node.cost for known in self.nodes)

    def __repr__(self):
        rep : List[Tuple[int,int]] = list()
        for wrapper in self.nodes:
            rep.append(wrapper[0])
        return rep.__repr__()


class BeamFrontier():
    def __init__(self, width: int = sys.maxint):
        self.size : int = 0
        self.seen : int = 0
        self.nodes : List[Node] = list()
        self.width : int = width

    """ Adds the self.width lowest cost nodes from neighbors to the frontier """
    def update(self, neighbors: Iterable[Node]) -> None:
        heapq.heapify(neighbors)
        best_neighbors : List[Node] = heapq.nlargest(self.width, neighbors)
        # self.nodes = heapq.merge(self.nodes, best_neighbors)
        # replace with for loop
        self.size += len(best_neighbors)

    def pop(self) -> Node:
        return heapq.heappop(self.nodes)



    def _remove(self, node: Node) -> None:
        return self.nodes.remove(node)

    """ Returns true if a node exists in the frontier with the same state but lower cost then the given """
    def _index_lt(self, node:Node) -> int:
        for i, known in enumerate(self.nodes):
            if node.state == known.state and known.cost < node.cost:
                return i

    @singledispatchmethod
    def contains(self, state: Tuple[int,int]) -> bool:
        return any(node.state == state for node in self.nodes)
    
    @contains.register(Node)
    def contains(self, node: Node) -> bool:
        return any(node.state == frontier_node.state for frontier_node in self.nodes)

    """ Returns true if a node exists in the frontier with the same state but lower cost then the given """
    def _contains_lt(self, node:Node) -> bool:
        # Should we prioritize older states or recent states when a state is refound with the same cost?
        return any(node.state == known.state and known.cost < node.cost for known in self.nodes)

    def empty(self):
        return self.size == 0

    def __repr__(self):
        rep : List[Tuple[int,int]] = list()
        for wrapper in self.nodes:
            rep.append(wrapper[0])
        return rep.__repr__()
