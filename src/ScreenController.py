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
        pass

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

            self.side_bar = ButtonListController(
                [
                    Button('Breadth First Search', self.solve),
                ], 
                (640, 10), 30, (364, 50), 20, ButtonView
            )
            self.boardAnimator = None      

    def solve(self):
        solution = Search.bfs(State(), lambda state: state.is_final())
        self.commandsView.commands = solution
        self.boardAnimator = RobotAnimator(self.board, solution)
        self.boardView.robot = self.boardAnimator.robot
        self.commandsView.robot = self.boardAnimator.robot

        #    solution = Search.bfs(State(), lambda state: state.is_final())
        #    solution = Search.astar(State(), lambda state: state.is_final(), Heuristic.mandatory_directions)
        #    solution = Optimization.simulated_annealing(board.initial_guess(), Scheduler.exponential_multiplicative_cooling)
   
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
