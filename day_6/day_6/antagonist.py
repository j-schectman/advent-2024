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
from day_6.spy_space import SpySpace


class Vat(GamePiece):
    def __str__(self) -> str:
        return 'O'
    def passable(self) -> bool:
        return False

class Antagonist():
    def __init__(self):
        self.obstruction_locations: set[tuple[int,int]] = set()

    def on_advance(self, new_position: Position, guard: Guard, current_board: Board):
        # see if obstacle can cause loop break guard, add one right front of them
        cloned = copy.deepcopy(current_board)
        obstruction_position = new_position.adjust(guard.facing)
        
        if not cloned.in_bounds(obstruction_position):
            return
        # Can't put an obstruction where there already is one
        if not cloned.is_space_open(obstruction_position): 
            return 

        cloned.set(Vat(), copy.deepcopy(obstruction_position))
        actives: list[ActivePiece] = [ActivePiece(copy.deepcopy(new_position), copy.deepcopy(guard))]
        watcher = Watcher(current_board.height, current_board.width)
        game = Game([[]], cloned, actives)
        game.subscribe_to_run(watcher.on_run)
        game.subscribe_to_advance(watcher.on_advance)
        # print('running game with board:')
        # print(game.board)
        result = game.run()
        if result:
            self.obstruction_locations.add((obstruction_position.x, obstruction_position.y))

    def get_count(self) -> int:
        print(self.obstruction_locations)
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

    def on_advance(self, new_position: Position, guard: Guard, _: Board):
        if not self.guard_tracker.in_bounds(new_position):
            return 
        if self._detect_loop(new_position, guard.facing):
            # print(self.guard_tracker)
            self._in_loop = True
            return
        spy_space = self.guard_tracker.get(new_position)
        if isinstance(spy_space, SpySpace):
            spy_space.directions.add(guard.facing)
            self.guard_tracker.set(spy_space, new_position)
        else:
            raise ValueError("Never not spy space!")

    def on_run(self) -> bool:
        return self._in_loop
