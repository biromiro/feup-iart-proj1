import pygame
from src.graphics.Color import Color
from src.graphics.RobotView import RobotView
from src.graphics.FontCache import FontCache

class BoardView:
    FONT_PATH = 'resources/fonts/square_block.ttf'

    def __init__(self, board):
        self.board = board
        self.font = FontCache()
        self.robot = None

    def write_in_cell(self, display, text, board_position, cell_position, cell_size, color):
        font_size = int(cell_size * 0.95)
        font = self.font.get(BoardView.FONT_PATH, font_size)
        rendered_start = font.render(text, True, color)
        start_text_pos = (
            int(board_position[0] + cell_size*(cell_position[0] + 0.5)), 
            int(board_position[1] + cell_size*(cell_position[1] + 0.5) - font.get_descent()//2)
        )
        display.blit(rendered_start, rendered_start.get_rect(center=start_text_pos))

    def draw(self, display, position, size):
        WALL_THICKNESS = 5
        WALL_COLOR = Color.BLACK
        GRID_THICKNESS = 2
        GRID_COLOR = Color.LIGHT_GRAY
        TEXT_COLOR = Color.LIGHT_GRAY
        TEXT_START = 'S'
        TEXT_GOAL = 'F'
        
        boardx, boardy = position
        cell_size = min(size[0]//self.board.width, size[1]//self.board.height)
        width = cell_size * self.board.width
        height = cell_size * self.board.height

        self.write_in_cell(display, TEXT_START, position, self.board.start, cell_size, TEXT_COLOR)
        self.write_in_cell(display, TEXT_GOAL, position, self.board.goal, cell_size, TEXT_COLOR)
        
        for x in range(boardx + cell_size, boardx + width, cell_size):
            pygame.draw.line(display, GRID_COLOR, (x, boardy), (x, boardy+height), GRID_THICKNESS)
        for y in range(boardy + cell_size, boardy + height, cell_size):
            pygame.draw.line(display, GRID_COLOR, (boardx, y), (boardx+width, y), GRID_THICKNESS)
        
        for wall in self.board.vertical_walls:
            wallx = boardx + wall[0]*cell_size
            wally = boardy + wall[1]*cell_size
            pygame.draw.line(display, WALL_COLOR, (wallx, wally), (wallx, wally + cell_size), WALL_THICKNESS)
        for wall in self.board.horizontal_walls:
            wallx = boardx + wall[0]*cell_size
            wally = boardy + wall[1]*cell_size
            pygame.draw.line(display, WALL_COLOR, (wallx, wally), (wallx + cell_size, wally), WALL_THICKNESS)

        if self.robot is not None:
            robot_position = (
                int(boardx + cell_size*(self.robot.current_position[0] + 0.5)), 
                int(boardy + cell_size*(self.robot.current_position[1] + 0.5))
            )
            RobotView().draw(display, robot_position, (cell_size * 0.95, cell_size * 0.95))
