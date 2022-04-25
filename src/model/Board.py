from src.model.Direction import Direction

class Board:
    """Represents the maze."""

    def __init__(self, width, height, moves):
        self.width = width
        self.height = height
        self.preferred_moves = moves # optimal solution size
        self.start = (0, self.height - 1) # starting cell
        self.goal = (self.width - 1, 0) # finishing cell
        self.vertical_walls = set() # set of cells with a vertical wall on their left
        self.horizontal_walls = set() # set of cells with an horizontal wall above them
        self.add_borders()

    def add_wall(self, x, y, direction):
        """Adds a wall to the maze."""
        if direction == Direction.RIGHT:
            self.vertical_walls.add((x+1, y))
        elif direction == Direction.LEFT:
            self.vertical_walls.add((x, y))
        elif direction == Direction.UP:
            self.horizontal_walls.add((x, y))
        elif direction == Direction.DOWN:
            self.horizontal_walls.add((x, y+1))

    def add_borders(self):
        """Adds borders to the outside cells of the maze."""
        for x in range(self.width):
            self.horizontal_walls.add((x, 0))
            self.horizontal_walls.add((x, self.height))
        for y in range(self.height):
            self.vertical_walls.add((0, y))
            self.vertical_walls.add((self.width, y))

    def move(self, position, command):
        """Returns the position after moving in the given direction. If there is a wall the robot doesn't move."""
        x, y = position
        if not self.can_move(position, command):
            return x, y

        if command == Direction.RIGHT:
            return x+1, y
        elif command == Direction.LEFT:
            return x-1, y
        elif command == Direction.UP:
            return x, y-1
        elif command == Direction.DOWN:
            return x, y+1

    def can_move(self, position, command):
        """Checks whether the robot can move in the given direction."""
        x, y = position
        if command == Direction.RIGHT and (x+1, y) in self.vertical_walls:
            return False
        if command == Direction.LEFT and (x, y) in self.vertical_walls:
            return False
        if command == Direction.UP and (x, y) in self.horizontal_walls:
            return False
        if command == Direction.DOWN and (x, y+1) in self.horizontal_walls:
            return False
        return True

    def walk(self, commands):
        """Iterates over the positions taken by the robot when executing the given commands. Stops at the goal or when entering and endless loop."""
        position = self.start
        previous_iterations = set()

        if len(commands) == 0:
            yield position # even without commands, the robot at least appears at the start of the maze.
            return

        while position not in previous_iterations: # repeating the same starting position means the robot is stuck in an endless loop
            previous_iterations.add(position)
            for command in commands:
                yield position
                if position == self.goal:
                    return
                position = self.move(position, command)
        yield position
