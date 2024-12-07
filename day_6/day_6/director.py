from abc import abstractmethod

from day_6.board import Board
from day_6.guard import Guard
from day_6.position import Position


class Director():
    @abstractmethod
    def on_guard(self, new_position: Position, guard: Guard, current_board: Board):
        pass

    # if the game should stop for some reason
    @abstractmethod
    def should_stop(self) -> bool:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass
