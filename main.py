from models.Board import Board
from models.BoardAnimator import BoardAnimator
from models.Direction import Direction
from models.State import State


def loadProblem(file):
    width, height, moves = [int(value) for value in file.readline().split()]
    horizontal_walls = [tuple(int(x) for x in coords.split(','))
                        for coords in file.readline().split(';')]
    vertical_walls = [tuple(int(x) for x in coords.split(','))
                      for coords in file.readline().split(';')]

    board = Board(width, height, moves)
    for x, y in horizontal_walls:
        board.add_wall(x, y, Direction.LEFT)
    for x, y in vertical_walls:
        board.add_wall(x, y, Direction.UP)
    return board


with open("problems/1.txt", 'r') as f:
    board = loadProblem(f)
    board.display()
    state = State()
    state.commands = ['R', 'R', 'L', 'U']
    animator = BoardAnimator()
    state.walk(board, animator)
