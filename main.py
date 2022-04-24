from src.Board import Board
from src.BoardAnimator import BoardAnimator
from src.Direction import Direction
from src.Optimization import Optimization
from src.Scheduler import Scheduler
from src.Selection import Selection
from src.Crossover import Crossover
from src.Mutation import Mutation
from src.Termination import Termination
from src.State import State
from src.Search import Search
from src.Heuristic import Heuristic
from src.Graphics import Graphics


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

# with open("problems/20.txt", 'r') as f:
#    board = loadProblem(f)
#    board.display()
#    initialState = board.initial_guess()
#    # findBestState(board, state)
#    #solution = Search.bfs(initialState, lambda state: state.is_final())
#    # solution = Search.astar(
#    #    initialState, lambda state: state.is_final(), Heuristic.mandatory_directions)
#
#    solution = Optimization.simulated_annealing(
#        initialState, Scheduler.exponential_multiplicative_cooling)
#    animator = BoardAnimator()
#    board.walk(solution, animator)


def main():
    # Graphics().run()
    with open("problems/1.txt", 'r') as f:
        board = loadProblem(f)

    mutator = Mutation.mutate_percent(15, Mutation.random_corruption)
    terminator = Termination().optimal(4)
    hold_best = Selection.best_n(10)
    solution = Optimization.genetic_algorithms(Selection.generation_zero(
        50, 2, board), Selection.roulette, Crossover.random_origin, mutator, terminator, hold_best)

    print(solution)

    animator = BoardAnimator()
    board.walk(solution, animator)


if __name__ == "__main__":
    main()

# with open("problems/1.txt", 'r') as f:
#    board = loadProblem(f)
#    board.display()
#    initialState = board.initial_guess()
    #gen_zero = []
    # for _ in range(10):
    #    individual = State([], board)
    #    for _ in range(4):
    #        individual.commands.append(Direction.random())
    #    gen_zero.append(individual)

    #solution = Optimization.genetic_algorithms(gen_zero, random_selector, random_crosser, mutate_50, solution_1)
    # findBestState(board, state)
    #solution = Search.bfs(initialState, lambda state: state.is_final())
    # solution = Search.astar(
    #    initialState, lambda state: state.is_final(), Heuristic.mandatory_directions)

    # solution = Optimization.simulated_annealing(
    #    initialState, Scheduler.exponential_multiplicative_cooling)
#    animator = BoardAnimator()
#    board.walk(solution, animator)
