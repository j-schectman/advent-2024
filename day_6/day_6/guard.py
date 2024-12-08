from day_6.direction import Direction
from day_6.game_piece import GamePiece, MovablePiece
from day_6.position import Position
import uuid


def get_guard_direction(char: str) -> Direction:
    if char == '^':
        return Direction.UP
    if char == 'v':
        return Direction.DOWN
    if char == '>':
        return Direction.RIGHT
    if char == '<':
        return Direction.LEFT

    # Default to Up
    return Direction.UP


class Guard(GamePiece, MovablePiece):
    def __init__(self, facing: Direction):
        super().__init__()
        self.facing = facing
        self.id = uuid.uuid4()

    def __str__(self) -> str:
        if self.facing == Direction.LEFT:
            return '<'
        if self.facing == Direction.RIGHT:
            return '>'
        if self.facing == Direction.UP:
            return '^'
        if self.facing == Direction.DOWN:
            return 'v'
        return 'g'


    def turn_90(self):
        if self.facing == Direction.LEFT:
            return Direction.UP
        if self.facing == Direction.RIGHT:
            return Direction.DOWN
        if self.facing == Direction.UP:
            return Direction.RIGHT
        if self.facing == Direction.DOWN:
            return Direction.LEFT

        raise ValueError("should never be anything other than a valid enum")

    def move(self, pos: Position):
        return pos.adjust(self.facing)

    def adjust_move(self):
        self.facing = self.turn_90()
    
    def passable(self) -> bool:
        return True
