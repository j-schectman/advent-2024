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

def add_point_to_edge(p1: Point, p2: Point, possible_edges: list[set[Point]]):
    for edge in possible_edges:
        if p1 in edge:
            edge.add(p2)

def print_path(graph: Graph, path: list[Move]):
    g = copy.deepcopy(graph)
    for b in path:
        p, d = b
        x, y = p
        f = print_dir(d)
        g[x,y] = f
        p = b
    print(g)


def calc_value(path: list[Move]) -> int:
    prev: None | Move = None
    c = 0
    for p in path:
        if prev == None:
            prev = p
            continue
        _, dir = p
        _, odir = prev
        if odir != dir:
            c+= 1000
        else:
            c+=1
        prev = p
    return c


def build_path(edges: dict[Move, Move | None], end: Move) -> list[Move]:
    path = []
    current = end
    while current:
        path.append(current)
        current = edges[current]
    return list(reversed(path))

# Return value is completed path
def walk(graph: Graph, starting: Point):
    edges: defaultdict[Move, Move | None] = defaultdict(lambda: None)
    # next move, built path
    # current movement cost, Movement
    queue: list[tuple[int, Move]] = []
    score_map: defaultdict[Move, int | None] = defaultdict(lambda: None)

    best_score_path: tuple[int, Move] | None = None
    for dir in DIRECTIONS:
        move = (starting, dir)
        initial_score = 0
        if dir != Direction.right:
            initial_score = 1000
        edges[move] = None
        score_map[move] = initial_score
        heappush(queue, (initial_score, move))
    while queue:
        score, move = queue.pop()
        previous_score = score_map[move]
        point, move_direction = move

        co = graph[point]
        if co == END:
            if best_score_path is None or score < best_score_path[0]:
                best_score_path = (score, move)

        if previous_score is not None and previous_score < score:
            continue

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
            if not existing_score or total_score < existing_score:
                score_map[next_move] = total_score
                edges[next_move] = move
                heappush(queue, (total_score, next_move))
            
    if best_score_path is None:
        return None
    score, move = best_score_path
    return score, build_path(edges, move)
        

def process_part_1(path: str) -> int:
    graph = parse_input(path)
    st = find_start(graph)
    result = walk(graph, st)
    if not result:
        raise ValueError('NO PATH FOUND')

    score, p = result
    print_path(graph, p)
    
    return score

