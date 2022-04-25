import pygame
from src.controller.Controller import Controller
from src.graphics.CommandsInputView import CommandsInputView
from src.model.CommandsInput import InputState
from src.model.Direction import Direction

class CommandsInputController(Controller):
    def __init__(self, commands_input, position, size, callback):
        self.input = commands_input
        self.view = CommandsInputView(self.input)
        self.position = position
        self.size = size
        self.callback = callback
        self.focused = commands_input.state == InputState.FOCUSED
    
    def enable(self, focused=False):
        self.focused = focused
        self.input.enabled = True
        self.input.no_highlight()
        self.input.state = InputState.FOCUSED if focused else InputState.NORMAL

    def contains(self, pos):
        return (
            pos[0] >= self.position[0] and
            pos[0] <= self.position[0] + self.size[0] and
            pos[1] >= self.position[1] and
            pos[1] <= self.position[1] + self.size[1]
        )

    def on_mouse_press(self, pos):
        if self.contains(pos):
            self.input.state = InputState.CLICKED
        else:
            self.input.state = InputState.NORMAL
            self.focused = False
    
    def on_mouse_release(self, pos):
        if self.contains(pos):
            if self.input.state == InputState.CLICKED:
                self.input.state = InputState.FOCUSED
                self.focused = True
            self.input.state = InputState.HOVERED
        else:
            self.input.state = InputState.FOCUSED if self.focused else InputState.NORMAL

    def on_mouse_move(self, pos):
        if self.contains(pos):
            if self.input.state != InputState.CLICKED:
                self.input.state = InputState.HOVERED
        elif self.input.state:
            self.input.state = InputState.FOCUSED if self.focused else InputState.NORMAL

    def on_key_press(self, key):
        if not self.focused:
            return
        if key == pygame.K_u:
            self.input.commands.append(Direction.UP)
        elif key == pygame.K_d:
            self.input.commands.append(Direction.DOWN)
        elif key == pygame.K_l:
            self.input.commands.append(Direction.LEFT)
        elif key == pygame.K_r:
            self.input.commands.append(Direction.RIGHT)
        elif key == pygame.K_BACKSPACE:
            if len(self.input.commands) > self.input.hint_shown:
                self.input.commands.pop()
        elif key == pygame.K_RETURN:
            self.callback()

    def draw(self, display):
        self.view.draw(display, self.position, self.size)
