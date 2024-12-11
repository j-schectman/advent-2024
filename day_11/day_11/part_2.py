from collections import defaultdict
from typing import Optional
def blink(c: int) -> tuple[int, Optional[int]]:
    if c == 0:
        return (1, None)

    to_split = str(c)
    if len(to_split) % 2 == 0:
        mid = len(to_split) // 2
        f, s = to_split[:mid], to_split[mid:]

        return (int(f), int(s))

    return (c * 2024, None)


def load_stones(path: str) -> list[int]:
    with open(path, 'r') as file:
        lines = file.readlines()
        if len(lines) != 1:
            raise ValueError("ASDFASDF")

        raw_stones = lines[0]
        return [int(x) for x in raw_stones.split()]

def process_part_2(path: str) -> int:
    stones = load_stones(path)
    stone_map: defaultdict = defaultdict(int)
    for stone in stones:
        stone_map[stone] += 1
    for _ in range(75):
        new_map: defaultdict = defaultdict(int)
        for num, count in stone_map.items():
            n1, n2 = blink(num)
            new_map[n1] += count
            if n2 != None:
                new_map[n2] += count
        stone_map = new_map

    return sum([count for count in stone_map.values()])
