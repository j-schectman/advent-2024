from enum import Enum

def get_input(file_path: str) -> list[list[int]]:
    with open(file_path, 'r') as file:
        return [[int(x) for x in line.split()] for line in file]

class Safety(Enum):
    UNKNOWN = 0
    ASCENDING = 1
    DESCENDING = -1

def is_safe(first_num: int, second_num: int, direction: Safety) -> tuple[bool, Safety]:
        diff = first_num - second_num
        abs_diff = abs(diff) 
        if abs_diff > 3:
            return (False, direction)

        if abs_diff < 1:
            return (False, direction)

        match direction:
            case Safety.UNKNOWN:
                if diff > 0:
                    return (True, Safety.ASCENDING)
                return (True, Safety.DESCENDING)
            case Safety.ASCENDING:
                if diff < 0:
                    return (False, direction)
            case Safety.DESCENDING:
                if diff > 0:
                    return (False, direction)
        return (True, direction)

def validate_report_part(report: list[int]) -> tuple[bool, int]:
    direction = Safety.UNKNOWN
    for i, [first_num, second_num] in enumerate(zip(report, report[1:])):
        success, direction = is_safe(first_num, second_num, direction)
        if not success:
            return False, i
    return True, -1

def process_part_1(file_path: str) -> int:
    input = get_input(file_path)
    return sum(1 if validate_report_part(report)[0] else 0 for report in input)

def retry(report: list[int], failed_index: int) -> bool:
    for i in range(-1, 3):
        removal_index = failed_index + i
        updated_list = report[:removal_index] + report[removal_index+1:]
        newResult, _ = validate_report_part(updated_list)
        if newResult:
            return True

    return False

def process_part_2(file_path: str) -> int:
    input = get_input(file_path)
    count = 0
    for report in input:
        result, index = validate_report_part(report)
        if not result:
            if retry(report, index):
                count += 1
        else:
            count += 1
    return count

def run():
    print(process_part_1('data/puzzle.txt'))
    print(process_part_2('data/puzzle.txt'))
