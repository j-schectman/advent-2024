from day_6.direction import Direction


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def adjust(self, dir: Direction):
        x, y = dir.value
        return Position(self.x + x, self.y + y)
