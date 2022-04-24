from src.controller.Controller import Controller
from src.model.Robot import Robot

class RobotAnimator(Controller):
    STEP_DURATION_MS = 600

    def __init__(self, board, commands_input):
        self.commands_input = commands_input
        self.steps = board.walk(commands_input.commands)
        self.robot = Robot(next(self.steps))
        self.time = 0

    def update(self, timepassed):
        self.time += timepassed
        if self.time >= RobotAnimator.STEP_DURATION_MS:
            step = None
            try:
                step = next(self.steps)
            except StopIteration:
                self.robot.end_walk()
                self.commands_input.no_highlight()
                return True
            self.time -= RobotAnimator.STEP_DURATION_MS
            self.commands_input.highlight_next()
            self.robot.set_step(step, self.commands_input.highlight == 0)
        
        animation_fraction = min(self.time / RobotAnimator.STEP_DURATION_MS, 1)
        self.robot.set_current_position(RobotAnimator.ease_function(animation_fraction))
        return False

    @staticmethod
    def ease_function(x):
        x = min(x*1.2, 1)
        return 4 * x * x * x if x < 0.5 else 1 - pow(-2 * x + 2, 3) / 2
