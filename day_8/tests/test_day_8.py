from day_8.main import process_part_1, process_part_2


def test_part_1():
    result = process_part_1('data/example.txt')
    assert result == 14, f'oh noes {result} != 14'

def test_part_2():
    result = process_part_2('data/example.txt')
    assert result == 34, f'oh noes {result} != 34'

def test_simple_part_2():
    result = process_part_2('data/example_p2.txt')
    assert result == 9, f'oh noes {result} != 9'

