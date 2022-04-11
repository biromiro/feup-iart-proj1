class State:
    def __init__(self):
        self.commands = []

    def apply_command(self, position, command):
        x, y = position
        if command == 'R':
            return x+1, y
        if command == 'L':
            return x-1, y
        if command == 'U':
            return x, y-1
        if command == 'D':
            return x, y+1

    def walk(self, board, animator=None):
        start = board.start
        target = board.goal
        if start == target:
            return True
        position = start
        previous_iteration = None
        while position != previous_iteration:
            previous_iteration = position
            for commandIdx, command in enumerate(self.commands):
                if animator != None:
                    animator.frame(board, self.commands, position, commandIdx)
                position = self.apply_command(position, command)
                if position == target:
                    return True
        return False
