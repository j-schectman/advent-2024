def load_matrix(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [x.strip() for x in file.readlines()]

