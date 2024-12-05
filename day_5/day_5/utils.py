from dataclasses import dataclass
@dataclass
class ProcessedInput:
    rules: list[str]
    updates: list[str]

def process_input(input: list[str]) -> ProcessedInput:
    rules_str: list[str] = []
    updates_str: list[str] = []

    at_updates = False

    for line in input:
        if at_updates:
            updates_str.append(line.strip())
        elif not line or line == "" or len(line) == 0 or line == '\n':
            at_updates = True
        else:
            rules_str.append(line.strip())
    return ProcessedInput(rules_str, updates_str)

def get_updates(updates_list: list[str]) -> list[list[int]]:
    return [[int(i) for i in page.split(',')] for page in updates_list]

def is_page_update_valid(rules: dict[int, set[int]], updates: list[int]) -> bool:
    updated_pages: set[int] = set()
    for page in updates:
        after_pages = rules.get(page)
        if after_pages and len(updated_pages & after_pages) > 0:
            return False

        updated_pages.add(page)

    return True

def get_middle_page(pages: list[int]) -> int:
    return pages[len(pages)//2]

def get_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return file.readlines()
