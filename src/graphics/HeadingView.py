import pygame
from src.graphics.FontCache import FontCache
from src.graphics.Color import Color

class HeadingView:
    FONT_NAME = ['segoeui', 'helvetica', 'arial']
    COLOR = Color.BLACK
    FONT = FontCache(system_font=True)

    def __init__(self, text):
        self.text = text
    
    def draw(self, display, position, size):
        x, y = position
        width, height = size
        
        font = HeadingView.FONT.get(HeadingView.FONT_NAME, height)
        text = font.render(self.text, True, HeadingView.COLOR)
        display.blit(text, text.get_rect(midtop=(x + width//2, y + font.get_descent())))
