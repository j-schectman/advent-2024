from enum import Enum
Move = str
Warehouse = list[list[str]]
Point = tuple[int, int]

ROBOT = '@'
WALL = '#'
FLOOR = '.'
CRATE = 'O'

class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

def get_move_direction(m: str) -> Direction:
    if m == '>':
        return Direction.right
    if m == '<':
        return Direction.left
    if m == '^':
        return Direction.up
    if m == 'v':
        return Direction.down

    raise ValueError('Invalid move')

def process_input(path: str) -> tuple[Warehouse, list[Move]]:
    ware: Warehouse = []
    moves: list[Move] = []
    with open(path, 'r') as file:
        at_moves = False
        for line in file.readlines():
            if line == '\n' or line == None:
                at_moves = True
                continue
            
            if at_moves:
                moves.extend(line.strip())
            else:
                ware.append(list(line.strip()))
    return ware, moves

def get_robot_location(ware: Warehouse) -> Point:
    for y, row in enumerate(ware):
        for x, c in enumerate(row):
            if c == ROBOT:
                return x,y
    raise ValueError('no robot in warehouse')

def in_warehouse(ware: Warehouse, point: Point) -> bool:
    height = len(ware)
    if len(ware) < 1:
        raise ValueError('invalid warehouse size')
    width = len(ware[0])
    x,y = point
    return 0 <= x < width and 0 <= y < height

def add_dir(point: Point, dir: Direction) -> Point:
    x, y = point
    dx, dy = dir.value
    return x+dx, y+dy

def get_object(ware: Warehouse, point: Point) -> str:
    x, y = point
    return ware[y][x]

def set_object(ware: Warehouse, point: Point, o: str) -> Warehouse:
    x, y = point
    # Yes I know this is mutating, I'm lazy today
    ware[y][x] = o
    return ware

# Point is new location of object, None if it can't move
def move_object(ware: Warehouse, point: Point, dir: Direction):
    next_point = add_dir(point, dir)
    if not in_warehouse(ware, next_point):
        return ware

    cur_object = get_object(ware, point)
    next_object = get_object(ware, next_point)
    if next_object == FLOOR:
        set_object(ware, next_point, cur_object)
        set_object(ware, point, FLOOR)
        return 

    if next_object == WALL:
        return

    if next_object == CRATE:
        move_object(ware, next_point, dir)
        check = get_object(ware, next_point)
        # if it's open floor, gucci to change
        if check == FLOOR:
            set_object(ware, next_point, cur_object)
            set_object(ware, point, FLOOR)


def move_robot(ware: Warehouse, robot: Point, dir: Direction):
    move_object(ware, robot, dir)
    
def get_crates(ware: Warehouse) -> set[Point]:
    res: set[Point] = set()
    for y, row in enumerate(ware):
        for x, c in enumerate(row):
            if c == CRATE:
                res.add((x,y))
    return res

def process_part_1(path: str) -> int:
    ware, moves = process_input(path)
    robot = get_robot_location(ware)

    # print('starting warehouse')
    # for row in ware:
    #     print(row)
    for move in moves:
        dir = get_move_direction(move)
        move_robot(ware, robot, dir)
        robot = get_robot_location(ware)
        # print('moved')
        # for row in ware:
        #     print(row)
    crates = get_crates(ware)
    total = 0
    for crate in crates:
        x, y = crate
        total += x + y*100

    return total
