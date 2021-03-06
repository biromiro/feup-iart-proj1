import random
from src.controller.Controller import Controller
from src.model.Direction import Direction

class SolverAnimator(Controller):
    STEP_DURATION_MS = 1

    def __init__(self, solver, commands_input, obfuscate=False, preferred_moves=None, slow_down=False):
        self.obfuscate = obfuscate
        self.preferred_moves = preferred_moves
        self.commands_input = commands_input
        self.solver = solver
        self.time = 0
        self.slow_down = slow_down
        if self.obfuscate:
            self.real_step = None
            self.next_obfuscation = 10 if self.slow_down else 100

    def update(self, timepassed):
        self.time += timepassed
        max_iters = 1 if self.slow_down else 25 # forces a slowdown if framerate can't keep up
        while self.time >= SolverAnimator.STEP_DURATION_MS:
            if max_iters <= 0:
                self.time = 0
                return False
            max_iters -= 1
            step = None
            try:
                step = next(self.solver).commands
                self.real_step = step
                if self.obfuscate:
                    if self.next_obfuscation <= 0:
                        self.next_obfuscation = 10 if self.slow_down else 100
                        self.commands_input.commands = [Direction.random() for _ in range(self.preferred_moves)]
                    self.next_obfuscation -= 1
                else:
                    self.commands_input.commands = step
            except StopIteration:
                self.commands_input.commands = self.real_step
                return True
            self.time -= SolverAnimator.STEP_DURATION_MS
        
        return False
