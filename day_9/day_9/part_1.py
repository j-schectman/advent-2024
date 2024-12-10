from itertools import zip_longest
def get_raw_disk_map(path: str) -> str:
    with open(path, 'r') as file:
        lines = file.readlines()
        if not len(lines) == 1:
            raise ValueError('aooooaoooa')
        return lines[0].strip()

Block = tuple[int,int]
FreeSpace = list[Block]
DiskData = list[int | None]
class SpaceIterator():
    def __init__(self, free_space: FreeSpace):
        self.free_space = free_space
        self.free_space_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.free_space_index >= len(self.free_space):
            raise StopIteration
        start_index, length = self.free_space[self.free_space_index] 
        self.free_space[self.free_space_index] = (start_index + 1, length - 1)
        # If length was 0 when we got here, then skip this index
        if length == 0:
            self.free_space_index += 1
            return self.__next__()
        if length - 1 <= 0:
            self.free_space_index += 1

        return start_index

    def remove_last_block(self):
        self.free_space.pop()


class Disk():
    def __init__(self):
        self.disk: DiskData = []
        self.free_space: FreeSpace = []

    def add_block(self, id: int, block_length: int, free_space: int | None):
        for _ in range(block_length):
            self.disk.append(id)
        if free_space == None:
            return
        self.free_space.append((len(self.disk), free_space))
        for _ in range(free_space):
            self.disk.append(None)

def build_disk(raw: str)-> Disk:
    nums = [int(x) for x in raw]
    pairs = list(zip_longest(nums[::2], nums[1::2]))

    disk = Disk()
    
    for id, disk_info in enumerate(pairs):
        disk.add_block(id, disk_info[0], disk_info[1])
    return disk

def process_part_1(path: str) -> int:
    map = get_raw_disk_map(path)
    disk = build_disk(map)
    disk_data = disk.disk
    space = SpaceIterator(disk.free_space)
    for free_index in space:
        if free_index >= len(disk_data):
            break
        next_id = disk_data.pop()
        if next_id == None:
            while next_id == None:
                next_id = disk_data.pop()
            space.remove_last_block()
        # all free spaces have been removed
        data_at = disk_data[free_index]
        if not data_at == None:
            raise ValueError("Should never not be none")
        disk_data[free_index] = next_id
    total = 0
    for i, data in enumerate(disk_data):
        if data == None:
            continue
        total += i * data
    return total
