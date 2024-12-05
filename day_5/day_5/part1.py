from day_5.utils import (
        process_input, 
        is_page_update_valid, 
        get_middle_page,
        get_lines,
        get_updates,
        )

def build_rules(rules_list: list[str]) -> dict[int, set[int]]:
    rules_map: dict[int,set[int]] = {}
    for rule in rules_list:
        before, after = rule.split('|')
        followers = rules_map.get(int(before), set())
        followers.add(int(after))
        rules_map[int(before)] = followers
    return rules_map

def process_part1(file_path: str) -> int:
    lines = get_lines(file_path)
    processed = process_input(lines)
    rules = build_rules(processed.rules)
    updates = get_updates(processed.updates)
    count = 0
    for update in updates:
        if is_page_update_valid(rules, update):
            count += get_middle_page(update)
    return count
