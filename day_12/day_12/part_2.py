from typing import Union
from enum import Enum
from collections import defaultdict

Point = tuple[int, int]
Plot = set[Point]
Side = set[Point]
VERTICAL: set[Point] = { (0, -1), (0, 1) }
HORIZONTAL: set[Point] = { (1, 0), (-1, 0) }

class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)
DIRECTIONS: set[Direction] = { Direction.up, Direction.down, Direction.left, Direction.right }

def get_opposite_directions_from_side(direction: Direction) -> set[Point]:
    if direction == Direction.up or direction == Direction.down:
        return HORIZONTAL
    return VERTICAL

def add_point(node: Point, node2: Point) -> Point:
    x, y = node
    dx, dy = node2
    return (x + dx, y + dy)

def get_neighbors(node: Point) -> set[Point]:
    return set([add_point(node, dir.value) for dir in DIRECTIONS])

def in_graph(node: Point, graph: list[list[str]]) -> bool:
    if len(graph) < 1:
        raise ValueError('screetching noises')
    x, y = node
    return 0 <= x < len(graph) and 0 <= y < len(graph[0])

def side_direction(plant: Point, direction: Direction, plot: Plot) -> bool:
    neighbor = add_point(plant, direction.value)
    return neighbor in plot

def build_plot_from_plant(plant: Point, graph: list[list[str]]) -> Plot:
    queue: set[Point] = set([plant])
    x, y = plant
    plant_type = graph[y][x]
    plot: Plot = set()
    visited: set[Point] = set()
    while len(queue) > 0:
        next_plant = queue.pop()
        if next_plant in visited:
            continue
        visited.add(next_plant)
        nx, ny = next_plant
        if next_plant in plot:
            continue
        if graph[ny][nx] != plant_type:
            continue

        plot.add(next_plant)

        neighbors = [
                neighbor for neighbor in get_neighbors(next_plant) 
                if in_graph(neighbor, graph) and 
                not neighbor in plot
                ]
        for neighbor in neighbors:
            x, y = neighbor
            if graph[y][x] == plant_type:
                queue.add(neighbor)
    return plot

def build_side_from_plant(plant: Point, plot: Plot, side_dir: Direction):
    queue: set[Point] = set([plant])
    visited: set[Point] = set()
    side: Side = set()
    directions = get_opposite_directions_from_side(side_dir)
    while len(queue) > 0:
        next_plant = queue.pop()
        if next_plant in visited:
            continue
        visited.add(next_plant)
        # If there is a plant from the same plot in the same direction as the side, then don't add it
        if side_direction(next_plant, side_dir, plot):
            continue

        side.add(next_plant)
        for direction in directions:
            neighbor = add_point(next_plant, direction)
            if not neighbor in visited and neighbor in plot:
                queue.add(neighbor)
    return side

def build_sides(plot: Plot):
    # building_sides(plot)
    visited: defaultdict[Point, set[Direction]] = defaultdict(set)
    sides: list[Side] = []
    for plant in plot:
        for direction in DIRECTIONS:
            if direction in visited[plant]:
                continue
            side = build_side_from_plant(plant, plot, direction)

            if len(side) > 0:
                sides.append(side)
            for sp in side:
                visited[sp].add(direction)
            visited[plant].add(direction)
    return sides

def get_graph(path: str) -> list[list[str]]:
    with open(path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

def process_part_2(path: str) -> int:
    graph = get_graph(path)
    plots: list[tuple[Plot, list[Side]]] = []
    found_plants: set[Point] = set()
    for y, row in enumerate(graph):
        for x, _ in enumerate(row):
            if (x,y) in found_plants:
                continue
            
            plant_node = (x, y)
            plot = build_plot_from_plant(plant_node, graph)
            if len(plot) < 1:
                continue
            plots.append((plot, build_sides(plot)))
            found_plants |= plot

    total = 0
    for plot, sides in plots:
        # print(f'area: {len(plot)} perim: {len(sides)} total: {len(plot) * len(sides)}')
        total += len(plot) * len(sides)

    print(f'total: {total}')
    return total
