from day_11.part_1 import process_part_1


def test_part_1():
    result = process_part_1('data/example.txt')
    assert result == 55312, f'reee {result} != 55312'
