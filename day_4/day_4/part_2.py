from day_4.common import load_matrix
ValidStringsPart2 = ['MAS', 'SAM']

def validate_str(maybe_mas: str) -> bool:
    return any(maybe_mas == s for s in ValidStringsPart2)

def part_2(file_path: str) -> int:
    count = 0
    matrix = load_matrix(file_path)
    for i, row in enumerate(matrix):
        if i == 0 or i == len(matrix) - 1:
            continue

        for j, letter in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            
            if not letter == 'A':
                continue

            forward_str = ''
            forward_str += matrix[i-1][j-1]
            forward_str += letter # always A... Right?
            forward_str += matrix[i+1][j+1]

            backward_str = ''
            backward_str += matrix[i-1][j+1]
            backward_str += letter # always A... Right?
            backward_str += matrix[i+1][j-1]

            if validate_str(forward_str) and validate_str(backward_str):
                count += 1

    return count
