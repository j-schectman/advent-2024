from day_12.part_1 import process_part_1
from day_12.part_2 import process_part_2


# def test_part_1():
#     result = process_part_1('data/example.txt')
#     assert result == 140, f'{result} != 140'

#     result2 = process_part_1('data/example2.txt')
#     assert result2 == 1930, f'{result2}!=1930'

def test_part_2():
    result = process_part_2('data/example.txt')
    assert result == 80, f'{result} != 80'

    result2 = process_part_2('data/example2.txt')
    assert result2 == 1206, f'{result2}!=1206'

