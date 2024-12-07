from day_6.antagonist import Antagonist
from day_6.game import Game
from day_6.im_bad_at_this import part2

def get_lines(path) -> list[str]:
    with open(path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def process_day_6(path: str) -> int:
    lines = get_lines(path)
    game = Game(lines)
    game.run()
    return len(game.active_path)

def process_day_6_part_2(path: str) -> int:
    lines = get_lines(path)
    game = Game(lines)
    antagonist = Antagonist()
    game.subscribe_to_advance(antagonist.on_advance)
    game.run()
    return antagonist.get_count()

if __name__ == "__main__":
    # print(process_day_6('data/puzzle.txt'))
    # print(process_day_6_part_2('data/puzzle.txt'))
    # help 1928
    lines = get_lines('data/puzzle.txt')
    print(part2(lines))


