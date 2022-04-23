from src.solvers.Heuristic import Heuristic
from src.Direction import Direction
import random


class State:
    def __init__(self, commands, board):
        self.commands = commands
        self.board = board

    def __repr__(self):
        return self.commands.__repr__()

    def __lt__(self, other):
        return len(self.commands) < len(other.commands)

    def operator_plus(self, command):
        return State(self.commands + [command], self.board)

    def child_states(self):
        return [self.operator_plus(command) for command in Direction]

    def preferred_moves_neighbour(self):
        choice = 'change'

        if len(self.commands) > self.board.preferred_moves:
            choice = 'remove'
        elif len(self.commands) < self.board.preferred_moves:
            choice = 'add'

        return State(self.getCommands(choice), self.board)

    def random_neighbour(self):
        choice = random.choice(['change', 'add', 'remove'])

        if len(self.commands) == 0:
            choice = 'add'

        return State(self.getCommands(choice), self.board)

    def getCommands(self, choice):
        commands = self.commands.copy()

        if choice == 'change':
            commands[random.randint(
                0, len(self.commands) - 1)] = Direction.random()
        elif choice == 'add':
            commands.insert(random.randint(
                0, len(self.commands)), Direction.random())
        else:
            commands.pop(random.randint(0, len(self.commands) - 1))

        return commands

    def is_final(self):
        for position in self.board.walk(self.commands):
            if position == self.board.goal:
                return True
        return False

    def evaluate(self):
        return Heuristic.min_manhattan(self) * 100 + len(self.commands)

    @staticmethod
    def initial_guess(board):
        if board.preferred_moves:
            return State([Direction.random() for _ in range(board.preferred_moves)], board)
        return State([], board)
