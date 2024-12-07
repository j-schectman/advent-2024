from day_6.direction import Direction
from day_6.game_piece import GamePiece

class SpySpace(GamePiece):
    def __init__(self):
        super().__init__()
        self.directions: set[Direction] = set()

    def __str__(self) -> str:
        horizontal = {Direction.LEFT, Direction.RIGHT}
        vertical = {Direction.DOWN, Direction.UP}
        has_horizontal = self.directions & horizontal
        has_vertical = self.directions & vertical
        if has_vertical and has_horizontal:
            return '+'
        if has_vertical:
            return '|'
        if has_horizontal:
            return '-'
        return '.'
