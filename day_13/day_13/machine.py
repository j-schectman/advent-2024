from dataclasses import dataclass
import re

Point = tuple[int, int]
button_strip = re.compile(r'[Buton A: X\+Y Prize\=]')
@dataclass
class Machine:
    a: Point
    b: Point
    prize: Point

def to_thruple(lines: list[str]) -> tuple[str, str, str]:
    if len(lines) != 3:
        raise ValueError(f"Expected 3 items, got {len(lines)}")
    return tuple(lines) # type: ignore

def build_point(s: str) -> Point:
    x, y = map(int, s.split(','))
    return (x, y)

def build_machine(lines: tuple[str, str, str], add_to_prize: int = 0) -> 'Machine':
    button_a, button_b, prize = lines
    stripped_a = re.sub(button_strip, '', button_a)
    stripped_b = re.sub(button_strip, '', button_b)
    prize = re.sub(button_strip, '', prize)
    a = build_point(stripped_a)
    b = build_point(stripped_b)
    px, py = build_point(prize)

    return Machine(a, b, (px + add_to_prize, py + add_to_prize))

def build_machines(path: str, add: int = 0) -> list[Machine]:
    with open(path, 'r') as f:
        machines = []
        line_groups: list[tuple[str, str, str]] = []
        m_lines: list[str] = []
        for line in f:
            stripped = line.strip()
            if len(line) == 0 or line == '\n':
                line_groups.append(to_thruple(m_lines))
                m_lines = []
            else:
                m_lines.append(stripped)
        if len(m_lines) == 3:
            line_groups.append(to_thruple(m_lines))
        for lines in line_groups:
            machines.append(build_machine(lines, add))
    return machines
