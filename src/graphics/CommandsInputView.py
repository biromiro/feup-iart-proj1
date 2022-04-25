from src.graphics.FontCache import FontCache
from src.graphics.Color import Color
import pygame
from src.model.CommandsInput import InputState

class CommandsInputView:
    TEXT_COLOR = Color.BLACK
    HIGHLIGHT_COLOR = Color.WHITE
    HINT_COLOR = Color.GREEN
    FONT_PATH = 'resources/fonts/square_block.ttf'
    BACKGROUND_COLOR = {
        True: Color.WHITE,
        False: Color.LIGHT_GRAY,
    }
    BORDER_COLOR = {
        InputState.NORMAL: Color.LIGHT_GRAY,
        InputState.HOVERED: Color.PRIMARY_LIGHT,
        InputState.CLICKED: Color.PRIMARY_DARK,
        InputState.FOCUSED: Color.PRIMARY
    }
    SHADOW_COLOR = Color.GRAY
    COMMANDS_LIMIT = 50

    def __init__(self, commands_input):
        self.commands_input = commands_input
        self.font = FontCache()
        self.last_command_len = None
    
    def draw(self, display, position, size):
        x, y = position
        width, height = size
        pygame.draw.rect(display, CommandsInputView.SHADOW_COLOR, pygame.Rect(x+3, y+3, width, height), 0, 10)
        pygame.draw.rect(display, CommandsInputView.BACKGROUND_COLOR[self.commands_input.enabled], pygame.Rect(x, y, width, height), 0, 10)
        if self.commands_input.enabled:
            pygame.draw.rect(display, CommandsInputView.BORDER_COLOR[self.commands_input.state], pygame.Rect(x, y, width, height), 5, 10)

        commands = self.commands_input.commands
        if len(self.commands_input.commands) > CommandsInputView.COMMANDS_LIMIT:
            commands = self.commands_input.commands[:CommandsInputView.COMMANDS_LIMIT] + ['...']

        for idx, command in enumerate(commands):
            len_commands = min(CommandsInputView.COMMANDS_LIMIT, len(self.commands_input.commands))
            is_same_font = self.last_command_len == len_commands
            self.last_command_len = len_commands

            font = self.font.get(CommandsInputView.FONT_PATH, height) if not is_same_font else self.font.cache
            highlight = self.commands_input.highlight == idx or (self.commands_input.highlight > CommandsInputView.COMMANDS_LIMIT and idx == CommandsInputView.COMMANDS_LIMIT)
            color = CommandsInputView.HIGHLIGHT_COLOR if highlight else CommandsInputView.TEXT_COLOR
            if self.commands_input.enabled and idx < self.commands_input.hint_shown:
                color = CommandsInputView.HINT_COLOR
            text = font.render(str(command), True, color)

            tw = text.get_width()
            n = len_commands
            s = int((width - tw*n)/(n + 1))
            if s <= 5 and not is_same_font:
                s = 5
                th = int(height*(width - s*(n+1))/(n*tw))
                font = self.font.get(CommandsInputView.FONT_PATH, th)
            tx = x + tw//2 + s + idx*(s+tw)
            ty = y + (height - font.get_descent())//2
            display.blit(text, text.get_rect(center=(tx, ty)))
            
