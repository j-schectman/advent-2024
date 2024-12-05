from day_5.utils import (
        process_input, 
        is_page_update_valid, 
        get_middle_page,
        get_lines,
        get_updates,
        )

def fix_bad_pages(rules: dict[int, set[int]], pages: list[int]) -> list[int] | None:
    fixed = try_fix_bad_pages(rules, pages)
    if not len(fixed) == len(pages):
        return None
    return fixed

def try_fix_bad_pages(
        rules: dict[int, set[int]], 
        pages: list[int]) -> list[int]:
    if len(pages) < 2:
        return pages
    # find the first page who doesn't appear in any other rule sets before rules
    for i, page in enumerate(pages):
        total_set = set()
        other_pages = pages[:i] + pages[i+1:]
        for x in other_pages:
            total_set = total_set | rules.get(x, set())

        if page not in total_set:
            result = try_fix_bad_pages(rules, other_pages) + [page]
            return result
    return []

def build_after_rules(rules_list: list[str]) -> dict[int, set[int]]:
    rules_map: dict[int,set[int]] = {}
    for rule in rules_list:
        before, after = rule.split('|')
        followers = rules_map.get(int(before), set())
        followers.add(int(after))
        rules_map[int(before)] = followers
    return rules_map

def build_before_rules(rules_list: list[str]) -> dict[int, set[int]]:
    rules_map: dict[int,set[int]] = {}
    for rule in rules_list:
        before, after = rule.split('|')
        previewers = rules_map.get(int(after), set())
        previewers.add(int(before))
        rules_map[int(after)] = previewers
    return rules_map

def process_part2(file_path: str) -> int:
    lines = get_lines(file_path)
    processed = process_input(lines)
    before_rules = build_before_rules(processed.rules)
    after_rules = build_after_rules(processed.rules)
    updates = get_updates(processed.updates)
    count = 0
    for update in updates:
        if not is_page_update_valid(after_rules, update):
            fixed_pages = fix_bad_pages(before_rules, update)
            if fixed_pages:
                count += get_middle_page(fixed_pages)
    return count
