from day_5.part1 import process_part1
from day_5.part2 import process_part2
def test_part1():
    result = process_part1('data/example.txt')
    assert result == 143, f'Uh oh {result} !== 143'

def test_part2():
    result = process_part2('data/example.txt')
    assert result == 123, f'Uh oh {result} !== 123'
