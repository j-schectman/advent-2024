from day_4.part_1 import part_1
from day_4.part_2 import part_2

def test_day_4_part_1():
    result = part_1('data/example.txt')
    assert  result == 18, f'{result} should be 18'

def test_day_4_part_2():
    result = part_2('data/example.txt')
    assert result == 9, f'{result} should be 9'
