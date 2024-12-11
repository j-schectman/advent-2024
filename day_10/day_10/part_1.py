from dataclasses import dataclass
from collections import defaultdict
@dataclass(frozen = True)
class Node():
    # x,y
    location: tuple[int,int]
    height: int

    def is_leaf(self) -> bool:
        return self.height == 9

    def is_root(self) -> bool:
        return self.height == 0

class Graph():
    def __init__(self):
        self.edges: defaultdict[Node, set[Node]] = defaultdict(set)
        self.root_nodes: set[Node] = set()

    def __getitem__(self, node: Node) -> set[Node]:
        return self.edges[node]
    
    def add_edge(self, node1: Node, node2: Node):
        self.edges[node1].add(node2)

    def add_edges(self, node: Node, neighbors: set[Node]):
        for node_b in neighbors:
            if node_b.height - node.height:
                self.add_edge(node, node_b)

    def add_root(self, node: Node):
        self.root_nodes.add(node)


def get_neighbors(node: tuple[int, int], raw_graph: list[list[str]]) -> set[Node]:
    neighbors: set[Node] = set()
    x, y = node

    # above
    ya = y - 1
    # below
    yb = y + 1
    # left
    xl = x - 1
    # right
    xr = x + 1
    def add_if_number(y1: int, x1: int):
        char = raw_graph[y1][x1]
        if char.isnumeric():
            neighbors.add(Node((x1,y1), int(char)))
    if ya >= 0:
        add_if_number(ya,x)

    if yb < len(raw_graph):
        add_if_number(yb,x)

    if xl >= 0:
        add_if_number(y,xl)

    if xr < len(raw_graph[0]):
        add_if_number(y,xr)
    return neighbors


def injest_data(path: str) -> Graph:
    graph = Graph()
    raw_graph: list[list[str]] = []
    with open(path, 'r') as file:
        for y, line in enumerate(file.readlines()):
            raw_graph.append(list(line.strip()))

    print(raw_graph)
    for y, row in enumerate(raw_graph):
        for x, height in enumerate(row):
            if height.isnumeric():
                node = Node((x,y), int(height))
                neighbs = get_neighbors((x,y), raw_graph)
                graph.add_edges(node, neighbs)
                if node.height == 0:
                    graph.add_root(node)

    return graph

def traverse(root: Node, graph: Graph, visited: set[Node] = set()) -> int:
    nines = 0
    print('root', root)
    for node in graph[root]:
        print('visiting', node, 'for', root.height)
        if node in visited:
            print('already visited')
            continue
        if node.height == 9:
            print(' found 9')
            visited.add(node)
            nines += 1
        nines += traverse(node, graph, visited)

    return nines

def process_part_1(path: str) -> int:
    graph = injest_data(path)
    nines = 0
    for root in graph.root_nodes:
        print('testing root', root)
        result = traverse(root, graph)
        print(result)
        nines += result
    return nines
