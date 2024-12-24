
from day_17.part_1 import process_part_1
from day_17.part_2 import process_part_2


def test_part_1():
    result = process_part_1('data/example.txt')
    assert result.get_output() == '4,6,3,5,6,3,5,2,1,0'

def test_example_2():
    result = process_part_1('data/example_2.txt')
    assert result.reg_b == 1

def test_example_3():
    result = process_part_1('data/example_3.txt')
    assert result.get_output() == '0,1,2'

def test_example_4():
    result = process_part_1('data/example_4.txt')
    assert result.get_output() == '4,2,5,6,7,7,7,7,3,1,0'
    assert result.reg_a == 0

def test_example_5():
    result = process_part_1('data/example_5.txt')
    assert result.reg_b == 26

def test_example_6():
    result = process_part_1('data/example_6.txt')
    assert result.reg_b == 44354


def test_part_2():
    result = process_part_2('data/example_p_2.txt')
    assert result == 117440
