from models.Board import Board
from models.BoardAnimator import BoardAnimator
from models.Direction import Direction
from models.Optimization import Optimization
from models.Scheduler import Scheduler
from models.State import State
from models.Search import Search
from models.Heuristic import Heuristic


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


with open("problems/20.txt", 'r') as f:
    board = loadProblem(f)
    board.display()
    initialState = board.initial_guess()
    # findBestState(board, state)
    #solution = Search.bfs(initialState, lambda state: state.is_final())
    # solution = Search.astar(
    #    initialState, lambda state: state.is_final(), Heuristic.mandatory_directions)

    solution = Optimization.simulated_annealing(
        initialState, Scheduler.exponential_multiplicative_cooling)
    animator = BoardAnimator()
    board.walk(solution, animator)
