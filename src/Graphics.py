from re import A
import sys, pygame, math
from turtle import position
from src.Board import Board
from src.Direction import Direction

pygame.init()
pygame.font.init()

# UNUSED (TODO if never used delete)
def draw_dashed_line(surf, color, start, end, width=1, dash_length=10):
    ox, oy = start
    tx, ty = end
    dx, dy = tx-ox, ty-oy
    l = int(math.sqrt(dx**2 + dy**2))
    slopex, slopey = dx/l, dy/l

    for idx in range(0, l//dash_length, 2):
        sx, sy = ox + slopex*idx*dash_length, oy + slopey*idx*dash_length
        ex, ey = sx + slopex*dash_length, sy + slopey*dash_length

        pygame.draw.line(surf, color, (sx, sy), (ex, ey), width)

class Color:
    BLACK = pygame.Color(0, 0, 0)
    LIGHT_GRAY = pygame.Color(220, 220, 220)
    WHITE = pygame.Color(255, 255, 255)

class BoardView:
    def __init__(self, board):
        self.board = board

    def draw(self, screen, position, size):
        WALL_THICKNESS = 5
        WALL_COLOR = Color.BLACK
        GRID_THICKNESS = 2
        GRID_COLOR = Color.LIGHT_GRAY
        
        boardx, boardy = position
        cell_size = min(size[0]//self.board.width, size[1]//self.board.height)
        width = cell_size * self.board.width
        height = cell_size * self.board.height
        
        for x in range(boardx + cell_size, boardx + width, cell_size):
            pygame.draw.line(screen, GRID_COLOR, (x, boardy), (x, boardy+height), GRID_THICKNESS)
        for y in range(boardy + cell_size, boardy + height, cell_size):
            pygame.draw.line(screen, GRID_COLOR, (boardx, y), (boardx+width, y), GRID_THICKNESS)
        
        for wall in self.board.vertical_walls:
            wallx = boardx + wall[0]*cell_size
            wally = boardy + wall[1]*cell_size
            pygame.draw.line(screen, WALL_COLOR, (wallx, wally), (wallx, wally + cell_size), WALL_THICKNESS)
        for wall in self.board.horizontal_walls:
            wallx = boardx + wall[0]*cell_size
            wally = boardy + wall[1]*cell_size
            pygame.draw.line(screen, WALL_COLOR, (wallx, wally), (wallx + cell_size, wally), WALL_THICKNESS)

class CommandsView:
    TEXT_COLOR = Color.BLACK
    FONT = pygame.font.SysFont('ComicSans MS', 30)
    TEXT_UP = FONT.render('U', True, TEXT_COLOR)
    TEXT_DOWN = FONT.render('D', True, TEXT_COLOR)
    TEXT_LEFT = FONT.render('L', True, TEXT_COLOR)
    TEXT_RIGHT = FONT.render('R', True, TEXT_COLOR)

    def __init__(self, commands):
        self.commands = commands
    
    def get_text(self, command):
        if command == Direction.RIGHT:
            return CommandsView.TEXT_RIGHT
        elif command == Direction.UP:
            return CommandsView.TEXT_UP
        elif command == Direction.LEFT:
            return CommandsView.TEXT_LEFT
        elif command == Direction.DOWN:
            return CommandsView.TEXT_DOWN
    
    def draw(self, screen, position):
        x, y = position
        pygame.draw.rect(screen, (190, 200, 230), pygame.Rect(x, y, 600, 50))
        for command in self.commands:
            text = self.get_text(command)
            screen.blit(text, (x, y))
            x += 100

class Graphics:
    def __init__(self):
        self.framerate = 60
        self.width = 1024
        self.height = 720
        
        # DEBUG (TODO remove)
        def loadProblem(file):
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
        with open("problems/20.txt", 'r') as f:
            board = loadProblem(f)
            self.boardView = BoardView(board)
            self.commandsView = CommandsView([Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.UP, Direction.DOWN, Direction.DOWN])
    
    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        
        clock = pygame.time.Clock()
        timepassed = 0
        while True:
            self.event_handler()
            self.update(timepassed)
            self.draw(screen)
            pygame.display.flip()
            timepassed = clock.tick(self.framerate)
    
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()    

    def update(self, timepassed):
        pass

    def draw(self, screen):
        screen.fill(Color.WHITE)
        self.boardView.draw(screen, (20,10), (600, 600))
        self.commandsView.draw(screen, (20, 650))
