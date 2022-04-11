class State:
    def __init__(self):
        self.commands = []

    def walk(self, board, animator=None):
        start = board.start
        target = board.goal
        if start == target:
            return True
        position = start
        previous_iterations = []
        while position not in previous_iterations:
            previous_iterations.append(position)
            for commandIdx, command in enumerate(self.commands):
                if animator != None:
                    animator.frame(board, self.commands, position, commandIdx)
                position = board.move(position, command)
                if position == target:
                    return True
        return False
