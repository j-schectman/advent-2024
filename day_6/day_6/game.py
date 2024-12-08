import copy
from typing import Optional
from day_6.active_piece import ActivePiece
from day_6.board import Board
from day_6.game_piece import GamePiece
from day_6.guard import Guard, get_guard_direction
from day_6.obstruction import Obstruction
from day_6.position import Position
from day_6.space import Space
from typing import Callable

def build_game_piece(char: str) -> GamePiece:
    if char == '#':
        return Obstruction()
    
    if char in ['^', '>', '<', 'v']:
        return Guard(get_guard_direction(char))

    return Space()
        
class Game():
    def __init__(self, input: list[str], board: Optional[Board] = None, active_pieces: Optional[list[ActivePiece]] = []):
        height = len(input)
        if height == 0:
            raise ValueError("invalid game height")
        width = len(input[0])
        self.active_pieces: list[ActivePiece] = []
        self.active_path: set[str] = set()
        if board:
            self.board = board
            if active_pieces:
                self.active_pieces = active_pieces
        else:
            self.board = Board(height, width)
            self._build_board(input)
        self.on_advance: list[Callable[[Position, Guard, Board]]] = []
        self.on_run: list[Callable[[], bool]] = []


    def _build_board(self, input: list[str]):
        for y, row in enumerate(input):
            for x, char in enumerate(row):
                position = Position(x, y)
                self._init_piece(build_game_piece(char), position)

    def _init_piece(self, piece: GamePiece, position: Position):
        if isinstance(piece, Guard):
            self.active_pieces.append(ActivePiece(position, piece))
            self.active_path.add(f'{position}')
        self.board.set(piece, position)

    def _can_move_space(self, requested_position: Position) -> bool:
        if not self.board.in_bounds(requested_position):
            return True
        potential_space = self.board.get(requested_position)
        return potential_space.passable()

    def subscribe_to_advance(self, fn: Callable[[Position, Guard, Board], None]):
        self.on_advance.append(fn)

    def subscribe_to_run(self, fn: Callable[[], bool]):
        self.on_run.append(fn)

    def advance(self):
        adjusted_pieces: list[ActivePiece] = []
        for piece in self.active_pieces:
            current_piece = piece.piece
            current_position = piece.position
            requested_position = current_piece.move(current_position)

            can_move = self._can_move_space(requested_position)
            if not can_move:
                current_piece.adjust_move()
            else:
                piece.position = requested_position

            if self.board.in_bounds(piece.position):
                self.active_path.add(f"{piece.position}")
                adjusted_pieces.append(piece)
                self.board.set(Space(), current_position)
                self.board.set(current_piece, piece.position)

            for fn in self.on_advance:
                fn(copy.deepcopy(piece.position), current_piece, self.board)

        
        self.active_pieces = adjusted_pieces


    # returns TRUE if exited early
    def run(self) -> bool:
        while(len(self.active_pieces) > 0):
            self.advance()
            # Break if return true
            for fn in self.on_run:
                if fn():
                    return True

        return False
