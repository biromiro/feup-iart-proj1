import imp
from models.Direction import Direction


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

    def display(self, current=None):
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
                    if current != None and (x, y) == current:
                        print('.', end='')
                    elif (x, y) == self.goal:
                        print('F', end='')
                    elif (x, y) == self.start:
                        print('S', end='')
                    else:
                        print(' ', end='')
            print('')

    # def allowed(self, origin, direction):
    #    destination = self.move(origin, direction)
    #    return direction not in self.walls.get(origin, []) and opposite(direction) not in self.walls.get(destination, [])
