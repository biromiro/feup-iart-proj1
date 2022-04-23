from src.solvers.Scheduler import Scheduler
from src.solvers.Optimization import Optimization
from src.solvers.Heuristic import Heuristic
from src.ButtonListController import ButtonListController
from src.graphics.ButtonView import ButtonView
from src.solvers.Search import Search
from src.solvers.State import State
from src.Direction import Direction
from src.Board import Board
from src.RobotAnimator import RobotAnimator
from src.graphics import BoardView, CommandsView
from src.Controller import Controller
from src.Button import Button

class ScreenController(Controller):
    def __init__(self):
        # DEBUG (TODO remove)
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
        with open("resources/problems/1.txt", 'r') as f:
            self.board = loadProblem(f)
        
        self.boardView = BoardView(self.board)
        self.commandsView = CommandsView([])

        self.side_bar = None
        self.boardAnimator = None

        self.page_main()

    def page_main(self):
        self.boardView.robot = None
        self.commandsView.robot = None
        self.side_bar = ButtonListController(
            [
                Button('Breadth First Search', lambda: self.page_search_solve(Search.bfs)),
                Button('Iterative Deepening Search', lambda: self.page_search_solve(Search.it_deep)),
                Button('Greedy Search', lambda: self.page_heuristic(Search.greedy)),
                Button('A* Search', lambda: self.page_heuristic(Search.astar)),
                Button('Simulated Annealing', lambda: self.page_scheduler()),
                Button('Genetic Algorithm', lambda: print("TODO")),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView
        )
    
    def page_heuristic(self, algorithm):
        self.boardView.robot = None
        self.commandsView.robot = None
        self.side_bar = ButtonListController(
            [
                Button('Manhattan Distance', lambda: self.page_search_solve(algorithm, heuristic=Heuristic.min_manhattan)),
                Button('Mandatory Directions', lambda: self.page_search_solve(algorithm, heuristic=Heuristic.mandatory_directions)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=lambda: self.page_main(),
            title="Choose heuristic:",
        )
    
    def page_scheduler(self):
        self.boardView.robot = None
        self.commandsView.robot = None
        self.side_bar = ButtonListController(
            [
                Button('Exponential Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.exponential_multiplicative_cooling)),
                Button('Logarithmic Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.logarithmical_multiplicative_cooling)),
                Button('Linear Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.linear_multiplicative_cooling)),
                Button('Quadratic Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.quadratic_multiplicative_cooling)),
                Button('Adaptive Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.adaptive_cooling, adaptive=True)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=lambda: self.page_main(),
            title="Choose schedule:",
        )

    def page_search_solve(self, algorithm, initial_state=None, is_final=None, **kwargs):
        initial_state = initial_state or State([], self.board)
        is_final = is_final or (lambda state: state.is_final())
        self.page_solve(algorithm(initial_state, is_final, **kwargs))

    def page_annealing_solve(self, schedule, initial_state=None, **kwargs):
        initial_state = initial_state or State.initial_guess(self.board)
        self.page_solve(Optimization.simulated_annealing(initial_state, schedule, **kwargs))

    def page_solve(self, solution):
        self.commandsView.commands = solution.commands
        self.boardAnimator = RobotAnimator(self.board, solution.commands)
        self.boardView.robot = self.boardAnimator.robot
        self.commandsView.robot = self.boardAnimator.robot
   
    def on_mouse_press(self, pos):
        self.side_bar.on_mouse_press(pos)
    
    def on_mouse_release(self, pos):
        self.side_bar.on_mouse_release(pos)

    def on_mouse_move(self, pos):
        self.side_bar.on_mouse_move(pos)

    def draw(self, display):
        self.boardView.draw(display, (20, 10), (600, 600))
        self.commandsView.draw(display, (20, 650), (600, 50))
        self.side_bar.draw(display)
    
    def update(self, timepassed):
        if self.boardAnimator:
            is_finished = self.boardAnimator.update(timepassed)
            if is_finished:
                self.boardAnimator = None
                # self.commandsView.commands = []
                # self.boardView.robot = None
                # self.commandsView.robot = None
