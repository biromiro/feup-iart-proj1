from src.graphics.FontCache import FontCache
from src.graphics.Color import Color
import pygame

class CommandsInputView:
    TEXT_COLOR = Color.BLACK
    HIGHLIGHT_COLOR = Color.WHITE
    FONT_PATH = 'resources/fonts/square_block.ttf'
    BACKGROUND_COLOR = Color.LIGHT_GRAY

    def __init__(self, commands_input):
        self.commands_input = commands_input
        self.font = FontCache()
        self.last_command_len = None
    
    def draw(self, display, position, size):
        x, y = position
        width, height = size
        pygame.draw.rect(display, Color.LIGHT_GRAY, pygame.Rect(x, y, width, height))

        for idx, command in enumerate(self.commands_input.commands):
            is_same_font = self.last_command_len == len(self.commands_input.commands)
            self.last_command_len = len(self.commands_input.commands)

            font = self.font.get(CommandsInputView.FONT_PATH, height) if not is_same_font else self.font.cache
            highlight = self.commands_input.highlight == idx
            color = CommandsInputView.HIGHLIGHT_COLOR if highlight else CommandsInputView.TEXT_COLOR
            text = font.render(str(command), True, color)

            tw = text.get_width()
            n = len(self.commands_input.commands)
            s = int((width - tw*n)/(n + 1))
            if s <= 5 and not is_same_font:
                s = 5
                th = int(height*(width - s*(n+1))/(n*tw))
                font = self.font.get(CommandsInputView.FONT_PATH, th)
            tx = x + tw//2 + s + idx*(s+tw)
            ty = y + (height - font.get_descent())//2
            display.blit(text, text.get_rect(center=(tx, ty)))
            
