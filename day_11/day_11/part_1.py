class Stone:
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def blink(self) -> list['Stone']:
        c = self.value
        if c == 0:
            return [Stone(1)]

        to_split = str(c)
        if len(to_split) % 2 == 0:
            mid = len(to_split) // 2
            f, s = to_split[:mid], to_split[mid:]

            return [Stone(int(f)), Stone(int(s))]

        return [Stone(c * 2024)]

def load_stones(path: str) -> list[Stone]:
    with open(path, 'r') as file:
        lines = file.readlines()
        if len(lines) != 1:
            raise ValueError("ASDFASDF")

        raw_stones = lines[0]
        return [Stone(int(x)) for x in raw_stones.split()]

def process_part_1(path: str) -> int:
    stones = load_stones(path)
    for _ in range(25):
        blunked = [x.blink() for x in stones]
        flattened = [stone for sub in blunked for stone in sub]
        stones = flattened

    return len(stones)
