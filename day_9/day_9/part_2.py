from itertools import zip_longest
def get_raw_disk_map(path: str) -> str:
    with open(path, 'r') as file:
        lines = file.readlines()
        if not len(lines) == 1:
            raise ValueError('aooooaoooa')
        return lines[0].strip()

Block = tuple[int,int]
FreeSpace = list[Block]
# id, block
DiskData = list[tuple[int, Block]]

class Space:
class Disk():
    def __init__(self):
        self.disk: DiskData = []
        # key is _size of block_
        self.space_map: dict[int, Block] = []
        self.disk_map: list[Block]
        self.size = 0

    def add_block(self, id: int, block_length: int, free_space: int | None):
        self.disk.append((id, (self.size, block_length)))
        for _ in range(block_length):
            self.disk_map.append(id)
        self.size += block_length
        if free_space == None:
            return
        self.free_space.append((self.size, free_space))

def build_disk(raw: str)-> Disk:
    nums = [int(x) for x in raw]
    pairs = list(zip_longest(nums[::2], nums[1::2]))

    disk = Disk()
    
    for id, disk_info in enumerate(pairs):
        disk.add_block(id, disk_info[0], disk_info[1])
    return disk

def process_part_2(path: str) -> int:
    map = get_raw_disk_map(path)
    disk = build_disk(map)
    disk_data = disk.disk
    free_space = disk.free_space
    index = 0
    free_space_index = 0
    disk_data_index = 0
    current_data_block = disk_data[0]
    while True:




    return 0
