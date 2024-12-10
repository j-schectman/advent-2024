from day_9 import part_1


def test_part_1():
    result = part_1.process_part_1('data/example.txt')
    assert result == 1928, f'oh no {result} != 1928'
