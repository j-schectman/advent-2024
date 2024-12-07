from dataclasses import dataclass

from day_6.guard import Guard
from day_6.position import Position


@dataclass
class ActivePiece():
    position: Position
    piece: Guard

