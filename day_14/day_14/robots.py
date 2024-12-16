import re
Point = tuple[int, int]
# Starting position, velocity
Robot = tuple[Point, Point]
strip_info = re.compile(r'[pv=]')

def build_point(s: str) -> Point:
    stripped_a = re.sub(strip_info, '', s)
    x, y = map(int, stripped_a.split(','))
    return (x, y)

def process_input(path: str) -> list[Robot]:
    robots: list[Robot] = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            p, v = line.strip().split(' ')
            robots.append((build_point(p), build_point(v)))
    return robots
