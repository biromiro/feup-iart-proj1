from models.Direction import Direction
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

    def random_neighbour(self):
        commandsCopy = self.commands.copy()

        choice = random.choice(['change', 'add', 'remove'])

        if len(commandsCopy) == 0:
            choice = 'add'

        if (choice == 'change'):
            commandsCopy[random.randint(
                0, len(self.commands) - 1)] = Direction.random()
        elif (choice == 'add'):
            commandsCopy.insert(random.randint(
                0, len(self.commands)), Direction.random())
        else:
            commandsCopy.pop(random.randint(0, len(self.commands) - 1))

        return State(commandsCopy, self.board)

    def is_final(self):
        return self.board.walk(self)[0]

    def evaluate(self):
        finished, distance = self.board.walk(self)

        max_distance = self.board.width + self.board.height

        return (max_distance + distance) * 100 + len(self.commands) if not finished else distance * 10 + len(self.commands)
