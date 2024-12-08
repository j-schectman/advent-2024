from collections import defaultdict
from itertools import combinations
from math import dist, sqrt
from typing import DefaultDict


Point = tuple[int, int]
# return value is the dictionary map and a height & width
def parse_input(path: str) -> tuple[dict[str, list[Point]], tuple[int,int]]:
    data_map: DefaultDict[str, list[Point]] = defaultdict(list)
    height = -1
    width = -1
    with open(path, 'r') as file:
        lines = file.readlines()
        height = len(lines)
        width = len(lines[0].strip())

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if char.isalnum():
                    antennas = data_map[char]
                    antennas.append((x,y))
                    data_map[char] = antennas
    return data_map, (height, width)

def get_antinode_distance_from_close_antenna(distance: Point, grid_size: Point) -> tuple[int, int] | None:
    dist_x, dist_y = distance
    height, width = grid_size

    x_anti = -1
    y_anti = -1
    
    xfound = False
    yfound = False
    for i in range(width):
        double_dist = dist_x + i
        if i*2 == double_dist:
            x_anti = i
            xfound = True
            break
    for i in range(height):
        double_dist = dist_y + i
        if i*2 == double_dist:
            y_anti = i
            yfound = True
            break

    if not yfound or not xfound:
        return

    return x_anti, y_anti

def is_oob(dimensions: Point, point: Point):
    x, y = point
    height, width = dimensions
    if x < 0:
        return True
    if x >= width:
        return True
    if y < 0:
        return True
    if y >= height:
        return True

    return False

def get_valid_antinodes(p1: Point, p2: Point, change: Point, dimensions: Point) -> set[Point]:
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = change

    y1_change = 0
    y2_change = 0
    x1_change = 0
    x2_change = 0
    if y1 > y2:
        y1_change = y1 + dy
        y2_change = y2 - dy
    else:
        y1_change = y1 - dy
        y2_change = y2 + dy

    if x1 > x2:
        x1_change = x1 + dx
        x2_change = x2 - dx
    else:
        x1_change = x1 - dx
        x2_change = x2 + dx

    results: set[Point] = set()
    if not is_oob(dimensions, (x1_change, y1_change)):
        results.add((x1_change, y1_change))

    if not is_oob(dimensions, (x2_change, y2_change)):
        results.add((x2_change, y2_change))
    return results


def process_part_1(file: str) -> int:
    data_map, dimensions = parse_input(file)
    antinodes: set[tuple[int,int]] = set()

    for _, locations in data_map.items():
        possible_lines = combinations(locations, 2)
        for p1, p2 in possible_lines:
            x1, y1 = p1
            x2, y2 = p2
            dist_x = abs(x1 - x2)
            dist_y = abs(y1 - y2)

            good_pos = get_antinode_distance_from_close_antenna((dist_x, dist_y), dimensions)
            if not good_pos:
                continue

            valid_anti = get_valid_antinodes(p1, p2, good_pos, dimensions)
            antinodes = antinodes | valid_anti
    return len(antinodes) 

def advance(travel: Point, times: int) -> Point:
    x, y = travel
    return (x * times, y * times)

def get_all_valid_antinodes(p1: Point, p2: Point, change: Point, dimensions: Point, i = 1) -> set[Point]:
    new_nodes =  get_valid_antinodes(p1,p2, advance(change,i), dimensions)
    if len(new_nodes) == 0:
        return set()
    return get_all_valid_antinodes(p1, p2, change, dimensions, i+1) | new_nodes

def process_part_2(file: str) -> int:
    data_map, dimensions = parse_input(file)
    antinodes: set[tuple[int,int]] = set()

    validation: defaultdict[str, set[Point]] = defaultdict(set)
    for c, locations in data_map.items():
        possible_lines = combinations(locations, 2)

        for p1, p2 in possible_lines:
            x1, y1 = p1
            x2, y2 = p2
            dist_x = abs(x1 - x2)
            dist_y = abs(y1 - y2)

            valid_anti = get_all_valid_antinodes(p1, p2, (dist_x, dist_y), dimensions) | {p1, p2}
            validation[c] = validation[c] | valid_anti
            antinodes = antinodes | valid_anti
    return len(antinodes) 

if __name__ == "__main__":
    print(process_part_1('data/puzzle.txt'))
    print(process_part_2('data/puzzle.txt'))
