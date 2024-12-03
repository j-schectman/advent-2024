import re
from functools import reduce

def get_str(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def multiply(mul: str) -> int:
    num_str = r'\d+'
    nums = [int(x) for x in re.findall(num_str, mul)]
    return reduce(lambda x, y: x * y, nums)

def process_day3(file_path: str) -> int:
    input = get_str(file_path)
    mul_string = r'mul\(\d+,\d+\)'
    muls = re.findall(mul_string, input)
    return reduce(lambda acc, cur: acc + multiply(cur), muls, 0)

def process_day3_part_2(file_path: str) -> int:
    input = get_str(file_path)
    inst_string = r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)'
    instructions = re.findall(inst_string, input)
    
    should_multiply: bool = True

    sum = 0
    for instruction in instructions:
        if instruction == 'do()':
            should_multiply = True
            continue

        if instruction == 'don\'t()':
            should_multiply = False
            continue

        if should_multiply:
            sum+= multiply(instruction)

    return sum


def day_3():
    print(process_day3('data/puzzle.txt'))
    print(process_day3_part_2('data/puzzle.txt'))
