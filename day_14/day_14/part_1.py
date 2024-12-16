from day_14.robots import Point, Robot, process_input
from collections import defaultdict
from math import prod

# Width, height
Grid = tuple[int, int]
def advance(robot: Robot, seconds: int) -> Robot:
    (px, py), (vx, vy) = robot
    return ((px + vx * seconds, py + vy * seconds), (vx, vy))

def get_grid_position(robot: Robot, grid: Grid) -> tuple[int, int]:
    (px, py), _ = robot
    width, height = grid
    return px % width, py % height

# quadrant can be 0-3
def calculate_quadrant(point: Point, grid: Grid) -> int | None:
    width, height = grid
    midx = width // 2
    midy = height // 2

    px, py = point
    if px < midx and py < midy:
        return 1

    if px > midx and py < midy:
        return 2

    if px < midx and py > midy:
        return 3

    if px > midx and py > midy:
        return 4

def part_1(path: str, grid: Grid) -> int:
    robots = process_input(path)
    positions: defaultdict[int, int]= defaultdict(int)
    for robot in robots:
        advanced = advance(robot, 100)
        position = get_grid_position(advanced, grid)
        quadrant = calculate_quadrant(position, grid)
        if quadrant:
            positions[quadrant] += 1

    return prod(positions.values())
