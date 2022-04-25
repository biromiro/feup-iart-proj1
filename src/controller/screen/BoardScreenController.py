import pygame
from src.controller.SolverAnimator import SolverAnimator
from src.model.CommandsInput import CommandsInput
from src.solvers.Crossover import Crossover
from src.solvers.Mutation import Mutation
from src.solvers.Scheduler import Scheduler
from src.solvers.Optimization import Optimization
from src.solvers.Heuristic import Heuristic
from src.controller.ButtonListController import ButtonListController
from src.graphics.ButtonView import ButtonView
from src.solvers.Search import Search
from src.solvers.Selection import Selection
from src.solvers.State import State
from src.controller.RobotAnimator import RobotAnimator
from src.graphics.BoardView import BoardView
from src.controller.Controller import Controller
from src.model.Button import Button
from src.controller.CommandsInputController import CommandsInputController
from src.solvers.Termination import Termination

class BoardScreenController(Controller):
    def __init__(self, _push_screen, board, human_player):
        self.board = board
        self.human_player = human_player
        
        self.board_view = BoardView(self.board)
        self.commands_panel = CommandsInputController(CommandsInput(human_player, human_player), (20, 650), (600, 50), self.page_animation)
        self.side_bar = None
        self.board_animator = None
        self.solver_animator = None

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
                Button('Genetic Algorithm', self.page_selector),
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
                Button('Linear Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.linear_cooling)),
                Button('Exponential Mult. Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.exponential_multiplicative_cooling)),
                Button('Logarithmic Mult. Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.logarithmical_multiplicative_cooling)),
                Button('Linear Mult. Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.linear_multiplicative_cooling)),
                Button('Quadratic Mult. Cooling', lambda: self.page_annealing_solve(schedule=Scheduler.quadratic_multiplicative_cooling)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=self.page_solvers,
            title="Choose schedule:",
        )

    def page_selector(self):
        self.side_bar = ButtonListController(
            [
                Button('Elitist cut 0.1', lambda: self.page_mutator(Selection.elitist(0.1))),
                Button('Elitist cut 0.3', lambda: self.page_mutator(Selection.elitist(0.3))),
                Button('Elitist cut 0.5', lambda: self.page_mutator(Selection.elitist(0.5))),
                Button('Elitist cut 0.7', lambda: self.page_mutator(Selection.elitist(0.7))),
                Button('Random', lambda: self.page_mutator(Selection.random_parents)),
                Button('Roulette', lambda: self.page_mutator(Selection.roulette)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=self.page_solvers,
            title="Choose selection:",
        )
    
    def page_mutator(self, selector):
        self.side_bar = ButtonListController(
            [
                Button('Mutate 10%', lambda: self.page_crosser(selector, Mutation.mutate_percent(10, Mutation.random_corruption))),
                Button('Mutate 25%', lambda: self.page_crosser(selector, Mutation.mutate_percent(25, Mutation.random_corruption))),
                Button('Mutate 50%', lambda: self.page_crosser(selector, Mutation.mutate_percent(50, Mutation.random_corruption))),
                Button('Mutate 75%', lambda: self.page_crosser(selector, Mutation.mutate_percent(75, Mutation.random_corruption))),
                Button('Mutate 90%', lambda: self.page_crosser(selector, Mutation.mutate_percent(90, Mutation.random_corruption))),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=self.page_selector,
            title="Choose mutation:",
        )

    def page_crosser(self, selector, mutator):
        self.side_bar = ButtonListController(
            [
                Button('Random origin', lambda: self.page_genetic_solve(selector, mutator, Crossover.random_origin)),
                Button('Split', lambda: self.page_genetic_solve(selector, mutator, Crossover.split)),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
            back_action=lambda: self.page_mutator(selector),
            title="Choose crossover:",
        )

    def page_search_solve(self, algorithm, initial_state=None, is_final=None, **kwargs):
        initial_state = initial_state or State([], self.board)
        is_final = is_final or (lambda state: state.is_final())
        self.page_solve(algorithm(initial_state, is_final, **kwargs))

    def page_annealing_solve(self, schedule, initial_state=None, **kwargs):
        initial_state = initial_state or State.initial_guess(self.board)
        self.page_solve(Optimization.simulated_annealing(initial_state, schedule, **kwargs))

    def page_genetic_solve(self, selector, mutator, crosser):
        self.page_solve(
            Optimization.genetic_algorithms(
                Selection.generation_zero(25, self.board.preferred_moves, self.board), 
                selector, 
                crosser, 
                mutator, 
                Termination().iteration_cap(256), 
                Selection.best_n(1)
            ),
            slow_down=True
        )

    def page_solve(self, solver, slow_down=False):
        current_commands = self.commands_panel.input.commands
        self.commands_panel.input.enabled = False
        self.solver_animator = SolverAnimator(solver, self.commands_panel.input, self.human_player, self.board.preferred_moves, slow_down=slow_down)

        def cancel():
            self.solver_animator = None
            self.commands_panel.input.commands = current_commands
            if self.human_player:
                self.commands_panel.enable(True)
                self.page_human()
            else:
                self.page_solvers()

        self.side_bar = ButtonListController(
            [
                Button('Cancel solver', cancel),
            ], 
            (640, 10), 30, (364, 50), 20, ButtonView,
        )

    def page_solution(self, solution):
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
        if self.solver_animator:
            is_finished = self.solver_animator.update(timepassed)
            if is_finished:
                self.solver_animator = None
                self.commands_panel.enable(True)
                self.page_solution(self.commands_panel.input)
