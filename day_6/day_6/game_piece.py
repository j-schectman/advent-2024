from abc import abstractmethod

from day_6.position import Position
class GamePiece():
    def __init__(self):
        pass

    @abstractmethod
    def passable(self) -> bool:
        pass

class MovablePiece():
     @abstractmethod
     def move(self, pos: Position) -> Position:
         pass
     
     # When move isn't available)
     @abstractmethod
     def adjust_move(self):
         pass

