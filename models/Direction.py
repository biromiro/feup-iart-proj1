from enum import Enum, auto


class Direction(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()

    def __repr__(self):
        if self == Direction.RIGHT:
            return 'R'
        elif self == Direction.UP:
            return 'U'
        elif self == Direction.LEFT:
            return 'L'
        elif self == Direction.DOWN:
            return 'D'
