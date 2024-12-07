def parse_tuples_from_file(filename):
    """
    Parse a file containing tuples in text format and return a set of tuples.
    Expects tuples in format like (1,5) with one tuple per line.
    
    Args:
        filename (str): Path to the input file
        
    Returns:
        set: Set of tuples parsed from the file
    """
    tuples = set()
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Remove whitespace and parentheses
                raw_tupes: list[str] = line.strip().split('),')
                for raw_tupe in raw_tupes:
                    nums = raw_tupe.strip(' ()')
                    numbers = tuple(int(x.strip()) for x in nums.split(','))
                    tuples.add(numbers)
    except ValueError as e:
        print(f"Error parsing number in file {filename}: {e}")
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
    return tuples

def compare_tuple_files(file1, file2):
    """
    Compare two files containing tuples and return the differences.
    
    Args:
        file1 (str): Path to first file
        file2 (str): Path to second file
        
    Returns:
        dict: Dictionary containing:
            - 'unique_to_file1': tuples only in first file
            - 'unique_to_file2': tuples only in second file
    """
    tuples1 = parse_tuples_from_file(file1)
    tuples2 = parse_tuples_from_file(file2)
    
    print(tuples2 & tuples1)
    print(f'overlap {len(tuples2 & tuples1)}')
    
    return {
        'unique_to_file1': tuples1 - tuples2,
        'unique_to_file2': tuples2 - tuples1
    }

if __name__ == "__main__":
    # Example usage
    file1_path = "foo.txt"
    file2_path = "foo2.txt"
    
    differences = compare_tuple_files(file1_path, file2_path)
    
    # print(f"\nTuples unique to {file1_path}:")
    # for tuple_item in sorted(differences['unique_to_file1']):
    #     print(tuple_item)
        
    # print(f"\nTuples unique to {file2_path}:")
    # for tuple_item in sorted(differences['unique_to_file2']):
    #     print(tuple_item)
    # print(f'total diff {len(differences["unique_to_file1"]) + len(differences["unique_to_file2"])}')
