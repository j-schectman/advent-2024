from day_6.game_piece import GamePiece
from day_6.position import Position
from day_6.space import Space

BoardType = list[list[GamePiece]]

class Board():
    def __init__(self, height: int, width: int):
        self.width = width
        self.height = height
        self.board = self._init_board()

    def __str__(self) -> str:
        grid = ""
        for _, row in enumerate(self.board):
            for _, char in enumerate(row):
                grid = f'{grid}{char}'
            grid += '\n'
        return grid

    def _init_board(self) -> BoardType:
        return [[Space] * self.width for _ in range(self.height)]

    def set(self, piece: GamePiece, position: Position):
        self.board[position.y][position.x]  = piece

    def get(self, position: Position) -> GamePiece:
        return self.board[position.y][position.x]

    def in_bounds(self, position: Position) -> bool:
        if position.x < 0 or position.y < 0:
            return False
        if position.x >= self.width:
            return False
        if position.y >= self.height:
            return False

        return True

    def is_space_open(self, position: Position) -> bool:
        return self.get(position).passable()
