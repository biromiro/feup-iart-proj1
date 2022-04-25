import imp
import random
from src.Direction import Direction
from src.State import State


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

    def initial_guess(self):
        if self.preferred_moves:
            return State([Direction.random() for _ in range(self.preferred_moves)], self)

        return State([], self)

    def empty_state(self):
        return State([], self)

    def walk(self, state, animator=None):
        start = self.start
        target = self.goal
        if start == target:
            return (True, 0)
        position = start
        previous_iterations = []
        bestDistance = self.width + self.height
        while position not in previous_iterations:
            previous_iterations.append(position)
            for commandIdx, command in enumerate(state.commands):
                if animator != None:
                    animator.frame(self, state.commands, position, commandIdx)
                position = self.move(position, command)
                if position == target:
                    return (True, 0)
                distance = abs(target[0] - position[0]) + \
                    abs(target[1] - position[1])
                if not bestDistance or bestDistance > distance:
                    bestDistance = distance
        return (False, bestDistance)
