from day_14.robots import Point, Robot, process_input
from collections import defaultdict
from math import prod

# Width, height
Grid = tuple[int, int]
def advance(robot: Robot, seconds: int, graph: Grid) -> Robot:
    (px, py), (vx, vy) = robot
    npx = px + vx * seconds
    npy = py + vy * seconds
    w, h = graph
    fpx = npx % w
    fpy = npy % h
    return ((fpx, fpy), (vx, vy))

def p_2_debug(robots: list[Robot], grid: Grid) -> None:
    w, h = grid
    g: list[list[int]] = []
    for y in range(h):
        g.append([])
        for _ in range(w):
            g[y].append(0)
    for robot in robots:
        advanced = advance(robot, 7672, grid)
        pos, _ = advanced
        x, y = pos
        g[y][x] += 1
    for y in range(h):
        line = ''
        for x in range(w):
            line += f'{g[y][x]}'
        print(line)

def part_2(path: str, grid: Grid) -> int:
    robots = process_input(path)
    positions: defaultdict[int, int]= defaultdict(int)
    w, h = grid
    nxt: list[Robot] = []
    for robot in robots:
        advanced = advance(robot, 97, grid)
        nxt.append(advanced)
    for i in range(2000):
        print('seconds ellapsed', (i+1) * 101 + 97)
        g: list[list[int]] = []
        next: list[Robot] = []
        for y in range(h):
            g.append([])
            for _ in range(w):
                g[y].append(0)
        
        for robot in nxt:
            advanced = advance(robot, 101, grid)
            next.append(advanced)
            pos, _ = advanced
            x, y = pos
            g[y][x] += 1
        for y in range(h):
            line = ''
            for x in range(w):
                line += f'{g[y][x]}'
            print(line)
        nxt = next
        print('\n')

    return prod(positions.values())
