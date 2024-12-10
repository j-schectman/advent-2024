from itertools import zip_longest
from dataclasses import dataclass

def get_raw_disk_map(path: str) -> str:
    with open(path, 'r') as file:
        lines = file.readlines()
        if not len(lines) == 1:
            raise ValueError('aooooaoooa')
        return lines[0].strip()

# first in is index, second is length
@dataclass
class Free():
    id: str
    index: int
    length: int

@dataclass
class File():
    id: int
    index: int
    length: int

Block = File | Free

FreeSpaceMap = list[Free]
Disk = list[Block]
def build_disk(raw: str) -> tuple[Disk, FreeSpaceMap]:
    nums = [int(x) for x in raw]
    pairs = list(zip_longest(nums[::2], nums[1::2]))

    disk = []
    free_space = []
    for id, disk_info in enumerate(pairs):
        block_size, free_size = disk_info
        disk.append(File(id, len(disk), block_size))
        if free_size is not None:
            current_index = len(disk)
            free_space.append(Free(f'free_{id}', current_index, disk_info[1]))
            disk.append(Free(f'free_{id}', current_index, free_size))
    return disk, free_space

def valid_move(block: Block, free: Free) -> bool:
    if not isinstance(free, Free):
        raise ValueError('should never be not free')

    return block.length <= free.length and block.index > free.index

def can_move(block: Block, free_space: FreeSpaceMap) -> int | None:
    new_index = next((x.index for x in free_space if valid_move(block, x)), None)
    return new_index

def consolidate(disk: Disk) -> tuple[Disk, FreeSpaceMap]:
    compacted_disk: Disk = []
    free_space: FreeSpaceMap = []
    current_free: Free | None = None
    for block in disk:
        if block.length == 0:
            continue
        if isinstance(block, Free):
            if current_free is None:
                current_free = block
            else:
                current_free.length += block.length
        else:
            if current_free is not None:
                current_free_index = len(compacted_disk)
                free_space.append(Free(current_free.id, current_free_index, current_free.length))
                compacted_disk.append(Free(current_free.id, current_free_index, current_free.length))
                current_free = None
            block.index = len(compacted_disk)
            compacted_disk.append(block)
    return compacted_disk, free_space

def compact_disk(disk: Disk, free_space: FreeSpaceMap, moved_list: set[int] = set()) -> tuple[Disk, FreeSpaceMap]:
    new_disk: list[Block] = []
    cannot_move: list[Block] = []

    moved = False
    adjusted_block: File | None = None
    adjusted_free: Free | None = None
    new_index: int | None = None
    run_again = True
    while(run_again):
        while(len(disk) > 0):
            next = disk.pop()
            if next is None:
                break

            if isinstance(next, Free):
                cannot_move.append(next)
                continue
            if next.id in moved_list:
                cannot_move.append(next)
                continue

            new_index = can_move(next, free_space)
            if new_index is not None:
                free_block = disk[new_index]
                if not isinstance(free_block, Free):
                    raise ValueError('oh no')
                cannot_move.append(Free(f'm_{next.id}', next.index, next.length))
                adjusted_block = File(next.id, new_index, next.length)
                adjusted_free = Free(free_block.id, new_index + 1, free_block.length - next.length)
                # fill old index with free
                moved = True
                break
            else:
                cannot_move.append(next)

            moved_list.add(next.id)
        if moved:
            for i, block in enumerate(disk):
                if i == new_index and adjusted_block is not None:
                    new_disk.append(adjusted_block)
                    if adjusted_free:
                        new_disk.append(adjusted_free)
                else:
                    new_disk.append(block)
            
            new_disk.extend(reversed(cannot_move))
            consolidated_disk, free_space = consolidate(new_disk)

            disk = consolidated_disk
            free_space = free_space
            new_disk = []
            cannot_move = []

            moved = False
            adjusted_block = None
            adjusted_free = None
            new_index = None
        else:
            run_again = False
    return list(reversed(cannot_move)), []

def pnd(disk: Disk) -> str:
    st = ''
    for block in disk:
        if isinstance(block, Free):
            for _ in range(block.length):
                st += '.'
        else:
            for _ in range(block.length):
                st += str(block.id)
    return st

def build_final(disk: Disk) -> list[int]:
    final = []
    for block in disk:
        for _ in range(block.length):
            if isinstance(block, Free):
                final.append(None)
            else:
                final.append(block.id)
    return final

def process_part_2(path: str) -> int:
    map = get_raw_disk_map(path)
    disk, free = build_disk(map)
    compacted_disk, _ = compact_disk(disk, free )
    total = 0
    for i, data in enumerate(build_final(compacted_disk)):
        if data == None:
            continue
        total += i * data
    return total
