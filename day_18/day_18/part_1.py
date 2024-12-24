from enum import IntEnum, auto
from collections import defaultdict

import copy

# BUILT WITH A LOT OF HELP FROM CLAUDE

START = 'S'
WALL = '#'
END = 'E'
Point = tuple[int, int]

class Direction(IntEnum):
    up = auto()
    down = auto()
    right = auto()
    left = auto()
    def get_point(self) -> Point:
        if self == Direction.up:
            return (0, -1)
        if self == Direction.down:
            return (0, 1)
        if self == Direction.left:
            return (-1, 0)
        if self == Direction.right:
            return (1, 0)
        raise ValueError('ah')

DIRECTIONS = [Direction.up, Direction.down, Direction.left, Direction.right]

def print_dir(dir: Direction) -> str:
    if dir == Direction.up:
        return '^'
    if dir == Direction.down:
        return 'v'
    if dir == Direction.left:
        return '<'
    if dir == Direction.right:
        return '>'

    raise ValueError('ah')


class Graph:
    def __init__(self, raw_lines: list[str]):
        if len(raw_lines) < 1:
            raise ValueError('invalid graph height')
        self.height = len( raw_lines )
        if len(raw_lines[0]) < 1:
            raise ValueError('invalid graph width')
        self.width = len(raw_lines[0])
        self.cells = [list(s) for s in raw_lines]
    
    def __getitem__(self, key: Point):
        if not isinstance(key, tuple) or len(key) != 2:
            raise KeyError("Access must be in the form graph[x,y]")
        x, y = key
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        return self.cells[y][x]
    
    def __setitem__(self, key: Point, value: str):
        if not isinstance(key, tuple) or len(key) != 2:
            raise KeyError("Access must be in the form graph[x,y]")
        x, y = key
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates out of bounds")
        self.cells[y][x] = value

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, self.cells[y][x])
    def __str__(self) -> str:
        t = ''
        for row in self.cells:
            t += ''.join(row) + '\n'
        return t


def parse_input(input_file: str) -> Graph:
    with open(input_file, 'r') as f:
        raw = [line.strip() for line in f]
        return Graph(raw)

def find_start(graph: Graph) -> Point:
    for x, y, s in graph:
        if s == START:
            return (x,y)
    raise ValueError('NO START FOUND')

def add_dir(point: Point, dir: Point) -> Point:
    x, y = point
    dx, dy = dir
    return x+dx, y+dy

def print_path(graph: Graph, path: list[Point]):
    g = copy.deepcopy(graph)
    for p in path:
        x, y = p
        g[x,y] = 'O'
    print(g)


# Current Move, Parent
Node = tuple[Point, 'Node | None']

def build_path(end: Node) -> list[Point]:
    path: list[Point] = []
    current = end
    while current:
        move, parent = current
        path.append(move)
        current = parent
        
    return list(reversed(path))

def build_visited_points(end: Node) -> set[Point]:
    move_set: set[Point] = set()
    current = end
    while current:
        move, parent = current
        move_set.add(move)
        current = parent
        
    return move_set


# Return value is completed path
def walk(graph: Graph, starting: Point):
    # next move, built path
    # current movement cost, Movement
    queue: list[tuple[int, Node]] = []
    score_map: defaultdict[Point, int | None] = defaultdict(lambda: None)
    best_nodes: list[Node] = []
    best_score: int | None = None

    best_score_path: tuple[int, Point] | None = None
    for dir in DIRECTIONS:
        move = starting
        initial_score = 0
        score_map[move] = initial_score
        queue.append((initial_score, (move, None)))
    while queue:
        score, node = queue.pop()
        move, _ = node

        # previous_score = score_map[move]
        point = move

        co = graph[point]
        if co == END:
            if best_score is None or score < best_score:
                best_nodes = [node]
                best_score = score
            if best_score is not None and score == best_score:
                best_nodes.append(node)

        # if previous_score is not None and previous_score < score:
        #     continue

        if best_score_path is not None and score >= best_score_path[0]:
            continue

        for dir in DIRECTIONS:
            next_point = add_dir(point, dir.get_point())
            # Don't need to check in bounds, maze is surrounded by walls
            if graph[next_point] == WALL:
                continue

            total_score = score + 1

            existing_score = score_map[next_point]
            if not existing_score or total_score <= existing_score:
                score_map[next_point] = total_score
                queue.append((total_score, (next_point, node)))
            
    if best_score is None:
        return None
    return best_score, best_nodes
        
def process_part_1(path: str, size: Point) -> int:

    graph = Graph([''])
    with open(path, 'r') as file:
        s_points = [line.strip() for line in file.readlines()]
        points = [(int(x), int(y)) for x, y in [point.split(',') for point in s_points]]
        for 

    return data
