from enum import Enum, auto
import random


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()
    UP = auto()

    @staticmethod
    def random():
        return random.choice(list(Direction))

    def __repr__(self):
        if self == Direction.RIGHT:
            return 'R'
        elif self == Direction.UP:
            return 'U'
        elif self == Direction.LEFT:
            return 'L'
        elif self == Direction.DOWN:
            return 'D'
