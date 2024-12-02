def get_inputs(file_path: str) -> tuple[list[int], list[int]]:
    list_one: list[int] = []
    list_two: list[int] = []
    with open(file_path, 'r') as file:
        # Or read line by line
        for line in file:
             a, b = line.split()
             list_one.append(int(a))
             list_two.append(int(b))
    return (list_one, list_two)
            
    
def process_file_part1(file_path: str) -> int: 
    list_one, list_two = get_inputs(file_path)
    sorted_one = sorted(list_one)
    sorted_two = sorted(list_two)
    result = sum(abs(x - y) for x, y in zip(sorted_one, sorted_two))
    return result

def process_file_part2(file_path: str) -> int:
    list_one, list_two = get_inputs(file_path)
    map_count: dict[int, int] = {}
    for i in list_two:
        cur: int = map_count.get(i, 0)
        map_count[i] = cur + 1

    result = sum(x * map_count.get(x,0) for x in list_one)
    return result


def puzzle() -> None:
    puzzle_input = 'data/puzzle_input.txt'
    print(f"Part 1 {process_file_part1(puzzle_input)}")
    print(f"Part 2 {process_file_part2(puzzle_input)}")
