import pygame
from src.model.CommandsInput import CommandsInput
from src.solvers.Scheduler import Scheduler
from src.solvers.Optimization import Optimization
from src.solvers.Heuristic import Heuristic
from src.controller.ButtonListController import ButtonListController
from src.graphics.ButtonView import ButtonView
from src.solvers.Search import Search
from src.solvers.State import State
from src.controller.RobotAnimator import RobotAnimator
from src.graphics.BoardView import BoardView
from src.controller.Controller import Controller
from src.model.Button import Button
from src.controller.CommandsInputController import CommandsInputController

class BoardScreenController(Controller):
    def __init__(self, _push_screen, board, human_player):
        self.board = board
        self.human_player = human_player
        
        self.board_view = BoardView(self.board)
        self.commands_panel = CommandsInputController(CommandsInput(human_player, human_player), (20, 650), (600, 50), self.page_animation)
        self.side_bar = None
        self.board_animator = None

        if self.human_player:
            self.page_human()
        else:
            self.page_solvers()

    def page_human(self):
        self.side_bar = ButtonListController(
            [
                Button('Run', self.page_animation),
                Button('Another hint', self.commands_panel.input.next_hint) if self.commands_panel.input.hint else Button('Hint', self.page_solvers),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
        )

    def page_solvers(self):
        self.side_bar = ButtonListController(
            [
                Button('Breadth First Search', lambda: self.page_search_solve(Search.bfs)),
                Button('Iterative Deepening Search', lambda: self.page_search_solve(Search.it_deep)),
                Button('Greedy Search', lambda: self.page_heuristic(Search.greedy)),
                Button('A* Search', lambda: self.page_heuristic(Search.astar)),
                Button('Simulated Annealing', self.page_scheduler),
                Button('Genetic Algorithm', lambda: print("TODO")),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            title="Choose solver:",
            back_action = self.page_human if self.human_player else None,
        )
    
    def page_heuristic(self, algorithm):
        self.side_bar = ButtonListController(
            [
                Button('Manhattan Distance', lambda: self.page_search_solve(algorithm, heuristic=Heuristic.min_manhattan)),
                Button('Mandatory Directions', lambda: self.page_search_solve(algorithm, heuristic=Heuristic.mandatory_directions)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=self.page_solvers,
            title="Choose heuristic:",
        )
    
    def page_scheduler(self):
        self.side_bar = ButtonListController(
            [
                Button('Exponential Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.exponential_multiplicative_cooling)),
                Button('Logarithmic Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.logarithmical_multiplicative_cooling)),
                Button('Linear Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.linear_multiplicative_cooling)),
                Button('Quadratic Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.quadratic_multiplicative_cooling)),
                Button('Adaptive Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.adaptive_cooling, adaptive=True)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=self.page_solvers,
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
        if self.human_player:
            self.commands_panel.input.hint = solution.commands
            self.commands_panel.input.next_hint()
            self.page_human()
        else:
            self.commands_panel.input.commands = solution.commands
            self.page_animation()
   
    def page_animation(self):
        if len(self.commands_panel.input.commands) == 0:
            return
        
        self.commands_panel.input.enabled = False
        self.board_animator = RobotAnimator(self.board, self.commands_panel.input)
        self.board_view.robot = self.board_animator.robot

        def stop_animation():
            self.board_view.robot = None
            self.board_animator = None
            if self.human_player:
                self.commands_panel.enable(True)
                self.page_human()
            else:
                self.commands_panel.input.no_highlight()
                self.page_solvers()

        self.side_bar = ButtonListController(
            [
                Button('Stop animation', stop_animation),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
        )

    def on_key_press(self, key):
        self.commands_panel.on_key_press(key)

    def on_mouse_press(self, pos):
        self.commands_panel.on_mouse_press(pos)
        self.side_bar.on_mouse_press(pos)
    
    def on_mouse_release(self, pos):
        self.commands_panel.on_mouse_release(pos)
        self.side_bar.on_mouse_release(pos)

    def on_mouse_move(self, pos):
        self.commands_panel.on_mouse_move(pos)
        self.side_bar.on_mouse_move(pos)

    def draw(self, display):
        self.board_view.draw(display, (20, 10), (600, 600))
        self.commands_panel.draw(display)
        self.side_bar.draw(display)
    
    def update(self, timepassed):
        if self.board_animator:
            is_finished = self.board_animator.update(timepassed)
            if is_finished:
                self.board_animator = None
