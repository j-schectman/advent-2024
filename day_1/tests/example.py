from d1 import main

def do_example():
    example_input = 'data/example_input.txt'
    result = main.process_file_part1(example_input)
    assert 11 == result, f"Expected {11} but got {result}"

    result2 = main.process_file_part2(example_input)
    assert 31 == result2, f"Expected {11} but got {result}"

