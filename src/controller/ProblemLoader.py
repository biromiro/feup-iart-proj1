import os
from src.model.Board import Board
from src.model.Direction import Direction

class ProblemLoader:
    FOLDER = "resources/problems"
    LOAD_ALL_CACHE = None

    @staticmethod
    def load_from_file(file):
        width, height, moves = [int(value) for value in file.readline().split()]
        horizontal_walls = [tuple(int(x) for x in coords.split(','))
                            for coords in file.readline().split(';')]
        vertical_walls = [tuple(int(x) for x in coords.split(','))
                        for coords in file.readline().split(';')]

        board = Board(width, height, moves)
        for x, y in horizontal_walls:
            board.add_wall(x, y, Direction.LEFT)
        for x, y in vertical_walls:
            board.add_wall(x, y, Direction.UP)
        return board
    
    @staticmethod
    def load_from_filename(filename):
        with open(os.path.join(ProblemLoader.FOLDER, filename), 'r') as f:
            return ProblemLoader.load_from_file(f)

    @staticmethod
    def load_all_files():
        if not ProblemLoader.LOAD_ALL_CACHE:
            ProblemLoader.LOAD_ALL_CACHE = [ProblemLoader.load_from_filename(file) for file in os.listdir(ProblemLoader.FOLDER)]
        return ProblemLoader.LOAD_ALL_CACHE
