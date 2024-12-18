from day_16.part_1 import process_part_1
from day_16.part_2 import process_part_2


# def test_part_1():
#     result = process_part_1('data/example.txt')
#     assert result == 7036
#     result = process_part_1('data/example2.txt')
#     assert result == 11048

def test_part_2():
    result = process_part_2('data/example.txt')
    assert result == 45
    result = process_part_2('data/example2.txt')
    assert result == 64
