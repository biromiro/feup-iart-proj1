from re import T

from regex import B
from src.graphics.FontCache import FontCache
from src.graphics.Color import Color
from src.Direction import Direction
from src.graphics.FontCache import FontCache
import pygame

class CommandsView:
    TEXT_COLOR = Color.BLACK
    HIGHLIGHT_COLOR = Color.WHITE
    FONT_PATH = 'resources/fonts/square_block.ttf'
    BACKGROUND_COLOR = Color.LIGHT_GRAY

    def __init__(self, commands):
        self.commands = commands
        self.robot = None
        self.font = FontCache()
        self.last_command_len = None
    
    def draw(self, display, position, size):
        x, y = position
        width, height = size
        pygame.draw.rect(display, Color.LIGHT_GRAY, pygame.Rect(x, y, width, height))

        for idx, command in enumerate(self.commands):
            is_same_font = self.last_command_len == len(self.commands)
            self.last_command_len = len(self.commands)

            font = self.font.get(CommandsView.FONT_PATH, height) if not is_same_font else self.font.cache
            highlight = self.robot and self.robot.command_idx == idx
            color = CommandsView.HIGHLIGHT_COLOR if highlight else CommandsView.TEXT_COLOR
            text = font.render(str(command), True, color)

            tw = text.get_width()
            n = len(self.commands)
            s = int((width - tw*n)/(n + 1))
            if s <= 5 and not is_same_font:
                s = 5
                th = int(height*(width - s*(n+1))/(n*tw))
                font = self.font.get(CommandsView.FONT_PATH, th)
            tx = x + tw//2 + s + idx*(s+tw)
            ty = y + (height - font.get_descent())//2
            display.blit(text, text.get_rect(center=(tx, ty)))
            
