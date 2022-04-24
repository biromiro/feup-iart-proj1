import pygame
from src.graphics.FontCache import FontCache
from src.model.Button import ButtonState
from src.graphics.Color import Color
from src.graphics.BoardView import BoardView

class BoardButtonView:
    FONT_NAME = ['segoeui', 'helvetica', 'arial']
    TEXT_COLOR = Color.BLACK
    BORDER_COLOR = {
        ButtonState.NORMAL: Color.WHITE,
        ButtonState.HOVERED: Color.PRIMARY_LIGHT,
        ButtonState.CLICKED: Color.PRIMARY_DARK
    }
    BACKGROUND_COLOR = Color.LIGHT_GRAY
    FONT = FontCache(system_font=True)

    def __init__(self, button):
        self.button = button
        self.board = BoardView(button.data)
    
    def draw(self, display, position, size, font_size):
        x, y = position
        width, height = size
        board_height = min(width//self.board.board.width, height - font_size//self.board.board.height) * self.board.board.height

        pygame.draw.rect(display, BoardButtonView.BACKGROUND_COLOR, pygame.Rect(x-10, y+board_height, width+20, height-board_height), 0, 15)
        pygame.draw.rect(display, BoardButtonView.BORDER_COLOR[self.button.state], pygame.Rect(x-10, y-10, width+20, height+20), 10, 15)
        
        self.board.draw(display, position, (width, height - font_size))
        

        font = BoardButtonView.FONT.get(BoardButtonView.FONT_NAME, font_size)
        text = font.render(f"{self.button.data.width}x{self.button.data.height}", True, BoardButtonView.TEXT_COLOR)
        display.blit(text, text.get_rect(center=(x + width//2, y + board_height + int(font_size*0.75))))
