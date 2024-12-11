Point = tuple[int, int]
Graph = list[list[str]]
DIRECTIONS: list[Point] = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def g_get(graph: Graph, point: Point) -> int:
    x, y = point
    c = graph[y][x]
    if c == '.':
        return -10
    return int(c)

def move(start: Point, change: Point) -> Point:
    x,y = start
    dx, dy = change
    return (x + dx, y + dy)

def get_neighbors(node: Point, graph: Graph) -> set[Point]:
    neighbors: set[Point] = set()
    height = len(graph)
    width = len(graph[0])
    for direction in DIRECTIONS:
        next_node = move(node, direction)
        x, y = next_node
        if 0 <= x < width and 0 <= y < height:
            neighbors.add(next_node)

    return neighbors

def injest_data(path: str) -> Graph:
    with open(path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()] 


def find_zeros(graph: Graph) -> set[Point]:
    result: set[Point] = set()
    for y, row in enumerate(graph):
        for x, char in enumerate(row):
            if char == '0':
                result.add((x,y))
    return result

def traverse(root: Point, graph: Graph) -> int:
    stack: list[Point] = [root]
    nine_count = 0
    while(len(stack) > 0):
        next = stack.pop()
        next_value = g_get(graph, next)
        if next_value == 9:
            nine_count += 1
            continue

        candidate_nodes = get_neighbors(next, graph)
        nodes = [node for node in candidate_nodes if g_get(graph, node) - next_value == 1]
        stack.extend(nodes)

    return nine_count

def process_part_2(path: str) -> int:
    graph = injest_data(path)
    nines = 0
    for root in find_zeros(graph):
        result = traverse(root, graph)
        nines += result
    return nines
