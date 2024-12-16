from enum import Enum
# from collections import defaultdict
Move = str
Warehouse = list[list[str]]
Point = tuple[int, int]
Crate = list[Point]

ROBOT = '@'
WALL = '#'
FLOOR = '.'
CRATE = 'O'
LEFT_CRATE = '['
RIGHT_CRATE = ']'
DCRATE = [LEFT_CRATE, RIGHT_CRATE]

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
    for row in ware:
        print(''.join(row))
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

def resize_warehouse(ware: Warehouse) -> Warehouse:
    new_house: Warehouse = []
    for row in ware:
        new_row: list[str] = []
        for c in row:
            if c == FLOOR:
                new_row.extend([ '.', '.' ])
            elif c == WALL:
                new_row.extend(['#','#'])
            elif c == CRATE:
                new_row.extend(['[',']'])
            elif c == ROBOT:
                new_row.extend(['@', '.'])
            else:
                raise ValueError('invalid character')
        new_house.append(new_row)

    return new_house

def get_partner_crate(ware: Warehouse, crate_side: Point) -> Point:
    cur_crate = get_object(ware, crate_side)
    if cur_crate == LEFT_CRATE:
        return add_dir(crate_side, Direction.right)
    if cur_crate == RIGHT_CRATE:
        return add_dir(crate_side, Direction.left)

    raise ValueError('invalid crate half')

def build_crate(ware: Warehouse, crate_side: Point) -> Crate:
    cur_crate = get_object(ware, crate_side)
    if cur_crate == LEFT_CRATE:
        return [crate_side, add_dir(crate_side, Direction.right)]
    if cur_crate == RIGHT_CRATE:
        return [add_dir(crate_side, Direction.left), crate_side]

    raise ValueError('invalid crate half')

def move_left(ware: Warehouse, points: list[Point]):
    # only need to worry about LEFT most item (smallest x)
    s = sorted(points)
    next_point = add_dir(s[0], Direction.left)
    next_object = get_object(ware, next_point)
    # Move all to the left, set the LAST item to be floor
    if next_object == FLOOR:
        for p in s:
            mp = get_object(ware, add_dir(p, Direction.left))
            set_object(ware, next_point, mp)
        set_object(ware, s[len(s) - 1], FLOOR)
        return 

    if next_object == WALL:
        return

    if next_object == CRATE:
        move_left(ware, build_crate(ware, next_point))
        check = get_object(ware, next_point)
        # if it's open floor, gucci to change
        if check == FLOOR:
            for p in s:
                mp = get_object(ware, add_dir(p, Direction.left))
                set_object(ware, next_point, mp)
            set_object(ware, s[len(s) - 1], FLOOR)


def move_right(ware: Warehouse, points: list[Point]):
    # only need to worry about RIGHT most item (largest x)
    s = sorted(points, reverse=True)
    next_point = add_dir(s[0], Direction.right)
    next_object = get_object(ware, next_point)
    # Move all to the left, set the LAST item to be floor
    if next_object == FLOOR:
        for p in s:
            mp = get_object(ware, add_dir(p, Direction.left))
            set_object(ware, next_point, mp)
        set_object(ware, s[len(s) - 1], FLOOR)
        return 

    if next_object == WALL:
        return

    if next_object == CRATE:
        move_left(ware, build_crate(ware, next_point))
        check = get_object(ware, next_point)
        # if it's open floor, gucci to change
        if check == FLOOR:
            for p in s:
                mp = get_object(ware, add_dir(p, Direction.left))
                set_object(ware, next_point, mp)
            set_object(ware, s[len(s) - 1], FLOOR)


# Point is new location of object, None if it can't move
def move_objects(ware: Warehouse, points: list[Point], dir: Direction):
    if dir == Direction.left:
        move_left(ware, points)
        return
    if dir == Direction.right:
        move_right(ware, points)
        return 

    # ALL next_points must be free to move ANY of the current points

    # if any of the future points aren't able to be moved, we can't move them, stay put
    # need to double up and handle crate points as well

    next_points: list[Point] = []
    for point in points:
        next_point = add_dir(point, dir)
        if not in_warehouse(ware, next_point):
            return 
        next_obj = get_object(ware, next_point)
        if next_obj == WALL:
            return 
        if next_obj in DCRATE:
            next_points.extend(build_crate(ware, next_point))
        else:
            next_points.append(next_point)

    # try moving the next set of objects
    move_objects(ware, next_points, dir)

    # after moving, ALL points must be open
    for next_point in next_points:
        ob = get_object(ware, next_point)
        if ob != FLOOR:
            return
    # Now move it
    for point in points:
        np = add_dir(point, dir)
        co = get_object(ware, point)
        set_object(ware, np, co)
        set_object(ware, point, FLOOR)

def move_robot(ware: Warehouse, robot: Point, dir: Direction):
    move_objects(ware, [robot], dir)
    
def get_crates(ware: Warehouse) -> set[Point]:
    res: set[Point] = set()
    for y, row in enumerate(ware):
        for x, c in enumerate(row):
            if c == CRATE:
                res.add((x,y))
    return res

def process_part_2(path: str) -> int:
    ware, moves = process_input(path)
    robot = get_robot_location(ware)
    rware = resize_warehouse(ware)

    print('starting warehouse')
    for row in rware:
        print(''.join(row))
    for move in moves:
        dir = get_move_direction(move)
        move_robot(rware, robot, dir)
        robot = get_robot_location(rware)
        print('moved')
        for row in rware:
            print(''.join(row))
    crates = get_crates(rware)
    total = 0
    for crate in crates:
        x, y = crate
        total += x + y*100

    return total
