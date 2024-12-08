from day_7.main import process_part_1, process_part_2

def test_part_1():
    result = process_part_1('data/example.txt')
    assert result == 3749, f'oh noooo {result} != 3749'

def test_part_2():
    result = process_part_2('data/example.txt')
    assert result == 11387, f'oh noooo {result} != 11387'
