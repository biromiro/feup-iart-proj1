from src.solvers.Heuristic import Heuristic
from src.model.Direction import Direction
import random


class State:
    """Represents a state in the state space. A state is a list of commands to be used by the robot on the maze."""
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
        """
        The child states of this state. A child state of a given state is the current list of commands 
        appended with a new command in one of the four possible directions.
        """
        return [self.operator_plus(command) for command in Direction]

    def preferred_moves_neighbour(self):
        """Randomly select a neighour that approximates the current state to the optimal number of moves."""
        choice = 'change'

        if len(self.commands) > self.board.preferred_moves:
            choice = 'remove'
        elif len(self.commands) < self.board.preferred_moves:
            choice = 'add'

        return State(self.getCommands(choice), self.board)

    def random_neighbour(self):
        """Randomly select a neighbor by adding, changing or removing an element from the list of commands. The choice of the action (add, remove, change) is random."""
        choice = random.choice(['change', 'add', 'remove'])

        if len(self.commands) == 0: # if there are no commands, it only makes sense to add a new command
            choice = 'add'

        return State(self.getCommands(choice), self.board)

    def getCommands(self, choice):
        """Randomly select a neighbor by adding, changing or removing an element from the list of commands."""
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
        """Check if this state is final."""
        for position in self.board.walk(self.commands):
            if position == self.board.goal: # if any position in the path of the robot is the goal, the state is final
                return True
        return False

    def evaluate(self):
        """Evaluation function."""
        return Heuristic.min_manhattan(self) * 100 + len(self.commands)

    @staticmethod
    def initial_guess(board):
        """Initial guess. Randomly initialize list with the optimal number of commands."""
        if board.preferred_moves:
            return State([Direction.random() for _ in range(board.preferred_moves)], board)
        return State([], board) # if the optimal number is unknown, the initial guess is an empty list
