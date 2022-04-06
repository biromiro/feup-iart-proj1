from enum import Enum, auto

class Direction(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()

class State:
    def __init__(self):
        self.commands = []
    
    def walk(self, board, start, target):
        if start == target:
            return True
        position = start
        previous_iteration = None
        while position != previous_iteration:
            previous_iteration = position
            for command in self.commands:
                position = command(position)
                if position == target:
                    return True
        return False

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start = (0, self.height - 1)
        self.goal = (self.width - 1, 0)
        self.vertical_walls = set()
        self.horizontal_walls = set()
        self.add_borders()
    
    def add_wall(self, x, y, direction):
        if direction == Direction.RIGHT:
            self.horizontal_walls.add((x+1, y))
        elif direction == Direction.LEFT:
            self.horizontal_walls.add((x, y))
        elif direction == Direction.UP:
            self.vertical_walls.add((x, y))
        elif direction == Direction.DOWN:
            self.vertical_walls.add((x, y+1))
    
    def add_borders(self):
        for x in range(self.width):
            self.horizontal_walls.add((x, 0))
            self.horizontal_walls.add((x, self.height))
        for y in range(self.height):
            self.vertical_walls.add((0, y))
            self.vertical_walls.add((self.width, y))

    def display(self):
        display_width = self.width*2 + 1
        display_height = self.height*2 + 1
        for j in range(display_height+1):
            for i in range(display_width+1):
                x = i//2
                y = j//2
                if i % 2 == 0 and j % 2 == 0:
                    print('+', end='')
                elif i % 2 == 0 and j % 2 == 1:
                    if (x, y) in self.vertical_walls:
                        print('|', end='')
                    else:
                        print(' ', end='')
                elif i % 2 == 1 and j % 2 == 0:
                    if (x, y) in self.horizontal_walls:
                        print('-', end='')
                    else:
                        print(' ', end='')
                else:
                    if (x, y) == self.start:
                        print('S', end='')
                    elif (x, y) == self.goal:
                        print('F', end='')
                    else:
                        print(' ', end='')
            print('')

    #def allowed(self, origin, direction):
    #    destination = self.move(origin, direction)
    #    return direction not in self.walls.get(origin, []) and opposite(direction) not in self.walls.get(destination, [])

board = Board(4, 5)
board.add_wall(2, 0, direction)
board.display()