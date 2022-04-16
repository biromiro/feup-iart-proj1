from models.Direction import Direction


class State:
    def __init__(self, commands, board):
        self.commands = commands
        self.board = board

    def __repr__(self):
        return self.commands.__repr__()

    def __lt__(self, other):
        return len(self.commands) < len(self.commands)

    def operator_plus(self, command):
        return State(self.commands + [command], self.board)

    def child_states(self):
        return [self.operator_plus(command) for command in Direction]

    def is_final(self):
        return self.board.walk(self)[0]
