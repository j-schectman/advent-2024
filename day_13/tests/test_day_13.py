from day_13.machine import build_machines
from day_13.part_1 import part_1


def test_machine():
    result = build_machines('data/example.txt')
    assert len(result) == 4
    first = result[0]
    assert first.a == (94, 34)
    assert first.b == (22, 67)
    assert first.prize == (8400, 5400)

def test_part_1():
    assert part_1('data/example.txt') == 480



