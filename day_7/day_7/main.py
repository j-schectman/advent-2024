from itertools import product
from functools import reduce
from typing import Callable

def process_line(line: str) -> tuple[int, list[int]]:
    number, to_sum = line.split(':')
    values = to_sum.split()
    return (int(number), [int(x) for x in values])

def handle_input(path: str) -> list[tuple[int, list[int]]]:
    with open(path, 'r') as file:
        return [process_line(line.strip()) for line in file.readlines()]

def mult(x: int, y: int) -> int:
    return x * y

def add(x: int, y: int) -> int:
    return x+y

def concat(x: int, y: int) -> int:
    return int(f'{x}{y}')

def can_equate(equation: tuple[int, list[int]], operators: list[Callable[[int,int],int]]) -> int:
    target, values = equation
    options = product(operators, repeat = len(values) - 1)
    def compute(acc: int, values: tuple[int, int]):
        i, num = values
        if i==0:
            return num
        return option[i-1](acc, num)

    for option in options:
        result = reduce(compute, list(enumerate(values)), 0)
        if result == target:
            return target

    return 0


def process_part_1(path: str) -> int:
    input = handle_input(path)
    return sum(can_equate(equation, [mult, add]) for equation in input)

def process_part_2(path: str) -> int:
    input = handle_input(path)
    return sum(can_equate(equation, [mult, add, concat]) for equation in input)

if __name__ == "__main__":
    print(process_part_1('data/puzzle.txt'))
    print(process_part_2('data/puzzle.txt'))
