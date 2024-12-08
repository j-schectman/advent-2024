# from day_6.direction import Direction
import copy
from day_6.active_piece import ActivePiece
from day_6.board import Board
from day_6.direction import Direction
from day_6.game_piece import GamePiece
from day_6.guard import Guard
from day_6.obstruction import Obstruction
from day_6.position import Position
from day_6.game import Game
from day_6.space import Space
from day_6.spy_space import SpySpace

bad_obs = {
(7, 44),
(10, 66),
(15, 72),
(17, 86),
(17, 91),
(17, 112),
(31, 67),
(34, 67),
(34, 72),
(36, 33),
(39, 26),
(39, 31),
(39, 65),
(41, 26),
(43, 72),
(45, 26),
(45, 65),
(47, 48),
(47, 65),
(47, 66),
(47, 67),
(47, 88),
(47, 112),
(48, 42),
(48, 50),
(48, 81),
(52, 81),
(55, 50),
(55, 65),
(55, 67),
(55, 72),
(56, 65),
(60, 28),
(60, 31),
(60, 43),
(60, 48),
(60, 50),
(60, 66),
(60, 75),
(60, 91),
(61, 48),
(61, 50),
(61, 65),
(61, 75),
(66, 65),
(66, 72),
(66, 81),
(70, 31),
(70, 43),
(70, 48),
(70, 62),
(70, 75),
(72, 62),
(74, 75),
(77, 66),
(77, 75),
(81, 66),
(83, 66),
(83, 75),
(85, 58),
(86, 80),
(92, 66),
(92, 69),
(92, 80),
(94, 66),
(96, 80),
(104, 109),
(116, 26),
(116, 66),
(120, 51)
}

class Vat(GamePiece):
    def __str__(self) -> str:
        return 'O'
    def passable(self) -> bool:
        return False

class Antagonist():
    def __init__(self):
        self.obstruction_locations: set[tuple[int,int]] = set()
        self.tried_locations: set[tuple[int,int]] = set()

    def on_advance(self, new_position: Position, facing: Guard, current_board: Board):
        # see if obstacle can cause loop break guard, add one right front of them

        obstruction_position = new_position.adjust(facing.facing)
        if (obstruction_position.x, obstruction_position.y) in self.tried_locations:
            return
        cloned = copy.deepcopy(current_board)
        
        if not cloned.in_bounds(obstruction_position):
            return
        # Can't put an obstruction where there already is one
        if not cloned.is_space_open(obstruction_position): 
            return 

        cloned.set(Vat(), copy.deepcopy(obstruction_position))

        actives: list[ActivePiece] = [ActivePiece(copy.deepcopy(new_position), Guard(facing.facing))]
        watcher = Watcher(current_board.height, current_board.width)
        game = Game([[]], cloned, actives)
        game.subscribe_to_run(watcher.on_run)
        game.subscribe_to_advance(watcher.on_advance)
        result = game.run()
        self.tried_locations.add((obstruction_position.x, obstruction_position.y))
        if result:
            global bad_obs
            if (obstruction_position.x, obstruction_position.y) in bad_obs:
                for y, row in enumerate(current_board.board):
                    for x, piece in enumerate(row):
                        if not isinstance(piece, Space):
                            watcher.guard_tracker.set(copy.deepcopy(piece), Position(x,y))
                watcher.guard_tracker.set(Vat(), obstruction_position)
                # print('guard tracker overlay')
                # print(watcher.guard_tracker)
            self.obstruction_locations.add((obstruction_position.x, obstruction_position.y))

    def get_count(self) -> int:
        return len(self.obstruction_locations)

class Watcher():
    def __init__(self, height: int, width: int):
        super().__init__()
        self.guard_tracker = Board(height, width)
        self._init_guard_tracker()
        self._in_loop = False

    def _init_guard_tracker(self):
        for y in range(self.guard_tracker.height):
            for x in range(self.guard_tracker.width):
                self.guard_tracker.set(SpySpace(), Position(x,y))

    def _detect_loop(self, new_position: Position, direction: Direction) -> bool:
        if not self.guard_tracker.in_bounds(new_position):
            return False
        cel = self.guard_tracker.get(new_position)
        if isinstance(cel, SpySpace):
            if direction in cel.directions:
                return True
        else:
            raise ValueError("should never not be a spy space")

        return False

    def on_advance(self, new_position: Position, facing: Guard, _: Board):
        if not self.guard_tracker.in_bounds(new_position):
            return 
        if self._detect_loop(new_position, facing.facing):
            self._in_loop = True
            return
        spy_space = self.guard_tracker.get(new_position)
        if isinstance(spy_space, SpySpace):
            spy_space.directions.add(facing.facing)
            self.guard_tracker.set(spy_space, new_position)
        else:
            raise ValueError("Never not spy space!")

    def on_run(self) -> bool:
        return self._in_loop
