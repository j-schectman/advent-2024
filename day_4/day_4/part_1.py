from day_4.common import load_matrix
ValidStrings = ['XMAS', 'SAMX']

def load_matrix(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [x.strip() for x in file.readlines()]

def validate_str(maybe_mas: str) -> bool:
    return any(maybe_mas == s for s in ValidStrings)

def sum_horizontal(matrix: list[str]) -> int:
    count = 0
    for row in matrix:
        for i, _ in enumerate(row):
            if validate_str(row[i:i+4]):
                count +=1
    return count

def sum_vertical(matrix: list[str]) -> int:
    count = 0
    for j, row in enumerate(matrix):
        if j > len(row) - 4:
            break

        for i, v in enumerate(row):
            s = ''
            s += v
            s += matrix[j+1][i]
            s += matrix[j+2][i]
            s += matrix[j+3][i]
            if validate_str(s):
                count += 1
    return count

def sum_diagonal(matrix: list[str]) -> int:
    count = 0
    for j, row in enumerate(matrix):
        if j > len(row) - 4:
            break

        for i, v in enumerate(row):
            if i < len(row) - 3:
                s = ''
                s += v
                s += matrix[j+1][i+1]
                s += matrix[j+2][i+2]
                s += matrix[j+3][i+3]
                if validate_str(s):
                    count += 1

            if i >= 3:
                s = ''
                s += v
                s += matrix[j+1][i-1]
                s += matrix[j+2][i-2]
                s += matrix[j+3][i-3]
                if validate_str(s):
                    count += 1

    return count

def part_1(file_path: str) -> int:
    matrix = load_matrix(file_path)
    return sum_diagonal(matrix) + sum_vertical(matrix) + sum_horizontal(matrix)
