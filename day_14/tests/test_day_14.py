from day_14.part_1 import part_1
from day_14.robots import process_input


def test_robot():
    result = process_input('data/example.txt')
    assert len(result) == 12
    assert result[0] == ((0, 4), (3, -3))

def test_part_1():
    result = part_1('data/example.txt', (11, 7))
    assert result == 12
