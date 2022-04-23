from src.Direction import Direction

class Board:
    def __init__(self, width, height, moves):
        self.width = width
        self.height = height
        self.preferred_moves = moves
        self.start = (0, self.height - 1)
        self.goal = (self.width - 1, 0)
        self.vertical_walls = set()
        self.horizontal_walls = set()
        self.add_borders()

    def add_wall(self, x, y, direction):
        if direction == Direction.RIGHT:
            self.vertical_walls.add((x+1, y))
        elif direction == Direction.LEFT:
            self.vertical_walls.add((x, y))
        elif direction == Direction.UP:
            self.horizontal_walls.add((x, y))
        elif direction == Direction.DOWN:
            self.horizontal_walls.add((x, y+1))

    def add_borders(self):
        for x in range(self.width):
            self.horizontal_walls.add((x, 0))
            self.horizontal_walls.add((x, self.height))
        for y in range(self.height):
            self.vertical_walls.add((0, y))
            self.vertical_walls.add((self.width, y))

    def move(self, position, command):
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
        position = self.start
        previous_iterations = set()

        if len(commands) == 0:
            yield position
            return

        while position not in previous_iterations:
            previous_iterations.add(position)
            for command in commands:
                yield position
                if position == self.goal:
                    return
                position = self.move(position, command)
