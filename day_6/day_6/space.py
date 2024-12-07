from day_6.game_piece import GamePiece

class Space(GamePiece):
    TypeGuard = GamePiece 
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return '.'

    def passable(self) -> bool:
        return True
