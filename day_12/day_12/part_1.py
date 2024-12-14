from typing import Union
import uuid

Point = tuple[int, int]

DIRECTIONS: list[Point] = [(0, -1), (0, 1), (1, 0), (-1, 0)]

def add_point(node: Point, node2: Point) -> Point:
    x, y = node
    dx, dy = node2
    return (x + dx, y + dy)

def get_neighbors(node: Point) -> set[Point]:
    return set([add_point(node, dir) for dir in DIRECTIONS])

def in_graph(node: Point, graph: list[list[str]]) -> bool:
    if len(graph) < 1:
        raise ValueError('screetching noises')
    x, y = node
    return 0 <= x < len(graph) and 0 <= y < len(graph[0])

class PlantNode:
    def __init__(self, plant_type: str, coords: Point):
        self.plant_type: str = plant_type
        self.coords = coords

    def __str__(self) -> str:
        return f'{self.plant_type}{self.coords[0]},{self.coords[1]}'

    def __eq__(self, other: object):
        if isinstance(other, tuple):
            return self.coords == other

        if not isinstance(other, PlantNode):
            return NotImplemented

        return self.coords == other.coords
    
    def __hash__(self):
        return hash(self.coords)

    def calc_perim(self, graph: list[list[str]]) -> int:
        return 4 - len(self.get_same_neighbors(graph))

    def get_same_neighbors(self, graph: list[list[str]]) -> set[Union['PlantNode', Point]]:
        points = get_neighbors(self.coords)
        valid_neighbors = set()
        for point in points:
            if not in_graph(point, graph):
                continue
            x, y = point
            if graph[y][x] == self.plant_type:
                valid_neighbors.add(PlantNode(self.plant_type, point))
        
        return valid_neighbors

class Plot:
    def __init__(self, plot_type: str, graph: list[list[str]]):
        self._graph = graph

        self.plot_type = plot_type
        self.nodes: set[PlantNode] = set()
        self.id = uuid.uuid4()

    def __eq__(self, other: object):
        if not isinstance(other, Plot):
            return NotImplemented

        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


    @property
    def area(self):
        return len(self.nodes)

    @property
    def perimiter(self):
        return sum([plant.calc_perim(self._graph) for plant in self.nodes])

    def add_plant(self, plant: PlantNode):
        if plant.plant_type != self.plot_type:
            raise ValueError(f'cannot add {plant.plant_type} to plot type {self.plot_type}')
        self.nodes.add(plant)

    def build_plot_from_plant(self, plant: PlantNode, graph: list[list[str]]):
        queue: set[PlantNode] = set([plant])
        while len(queue) > 0:
            next_plant = queue.pop()
            self.add_plant(next_plant)
            neighbors = get_neighbors(next_plant.coords)
            for neighbor in neighbors:
                if self.has_plant(neighbor) or neighbor in queue:
                    continue
                if not in_graph(neighbor, graph):
                    continue
                x, y = neighbor
                if graph[y][x] == self.plot_type:
                    queue.add(PlantNode(self.plot_type, neighbor))
        

    def has_plant(self, plant: Union[PlantNode , tuple[int,int]]) -> bool:
        return plant in self.nodes


def get_graph(path: str) -> list[list[str]]:
    with open(path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

def process_part_1(path: str) -> int:
    graph = get_graph(path)
    plots: set[Plot] = set()
    found_plants: set[PlantNode] = set()
    for y, row in enumerate(graph):
        for x, plant in enumerate(row):
            if (x,y) in found_plants:
                continue
            
            plant_node = PlantNode(plant, (x, y))
            plot = Plot(plant, graph)
            plot.build_plot_from_plant(plant_node, graph)
            plots.add(plot)
            found_plants |= plot.nodes

    total = 0
    for plot in plots:
        total += plot.area * plot.perimiter

    print(f'total: {total}')
    return total



