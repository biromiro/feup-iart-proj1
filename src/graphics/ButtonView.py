import pygame
from src.graphics.FontCache import FontCache
from src.model.Button import ButtonState
from src.graphics.Color import Color

class ButtonView:
    FONT_NAME = ['segoeui', 'helvetica', 'arial']
    TEXT_COLOR = Color.BLACK
    BACKGROUND_COLOR = {
        ButtonState.NORMAL: Color.PRIMARY,
        ButtonState.HOVERED: Color.PRIMARY_LIGHT,
        ButtonState.CLICKED: Color.PRIMARY_DARK
    }
    SHADOW_COLOR = Color.GRAY
    FONT = FontCache(system_font=True)

    def __init__(self, button):
        self.button = button
    
    def draw(self, display, position, size, font_size):
        x, y = position
        width, height = size
        pygame.draw.rect(display, ButtonView.SHADOW_COLOR, pygame.Rect(x+3, y+3, width, height), 0, 15)
        pygame.draw.rect(display, ButtonView.BACKGROUND_COLOR[self.button.state], pygame.Rect(x, y, width, height), 0, 15)
        
        font = ButtonView.FONT.get(ButtonView.FONT_NAME, font_size)
        text = font.render(self.button.data, True, ButtonView.TEXT_COLOR)
        display.blit(text, text.get_rect(center=(x + width//2, y + height//2)))
