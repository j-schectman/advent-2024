from enum import IntEnum, auto
from collections import defaultdict
from heapq import heappush

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

Move = tuple[Point, Direction]

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

def print_path(graph: Graph, path: list[Move]):
    g = copy.deepcopy(graph)
    for b in path:
        p, d = b
        x, y = p
        f = print_dir(d)
        g[x,y] = f
        p = b
    print(g)


# Current Move, Parent
Node = tuple[Move, 'Node | None']

def build_path(end: Node) -> list[Move]:
    path: list[Move] = []
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
        move_set.add(move[0])
        current = parent
        
    return move_set


# Return value is completed path
def walk(graph: Graph, starting: Point):
    # next move, built path
    # current movement cost, Movement
    queue: list[tuple[int, Node]] = []
    score_map: defaultdict[Move, int | None] = defaultdict(lambda: None)
    best_nodes: list[Node] = []
    best_score: int | None = None

    best_score_path: tuple[int, Move] | None = None
    for dir in DIRECTIONS:
        move = (starting, dir)
        initial_score = 0
        if dir != Direction.right:
            initial_score = 1000
        score_map[move] = initial_score
        heappush(queue, (initial_score, (move, None)))
    while queue:
        score, node = queue.pop()
        move, _ = node

        # previous_score = score_map[move]
        point, move_direction = move

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
            np = add_dir(point, dir.get_point())
            # Don't need to check in bounds, maze is surrounded by walls
            if graph[np] == WALL:
                continue

            movement_score = 1 + (1000 if dir != move_direction else 0)
            next_move = (np, dir)
            total_score = score + movement_score

            existing_score = score_map[next_move]
            if not existing_score or total_score <= existing_score:
                score_map[next_move] = total_score
                heappush(queue, (total_score, (next_move, node)))
            
    if best_score is None:
        return None
    return best_score, best_nodes
        

def process_part_2(path: str) -> int:
    graph = parse_input(path)
    st = find_start(graph)
    result = walk(graph, st)
    if not result:
        raise ValueError('NO PATH FOUND')

    _, best_nodes = result
    # for s in best_nodes:
    #     print_path(graph, build_path(s))

    distinct_points: set[Point] = set()
    for p in best_nodes:
        distinct_points |= set(build_visited_points(p))
    
    return len(distinct_points)
