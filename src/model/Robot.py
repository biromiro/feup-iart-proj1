class Robot:
    def __init__(self, position):
        self.from_position = position
        self.target_position = position
        self.current_position = position
        self.previous_iterations = []

    def set_step(self, position, add_to_previous_iterations=False):
        self.from_position = self.target_position
        self.current_position = self.from_position
        self.target_position = position
        if add_to_previous_iterations:
            self.previous_iterations.append(self.from_position)
        
    def set_current_position(self, fraction):
        self.current_position = (
            self.from_position[0] + (self.target_position[0] - self.from_position[0]) * fraction,
            self.from_position[1] + (self.target_position[1] - self.from_position[1]) * fraction
        )

    def end_walk(self):
        self.from_position = self.target_position
        self.current_position = self.from_position
