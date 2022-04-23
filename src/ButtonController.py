from src.Button import ButtonState
from src.Controller import Controller

class ButtonController(Controller):
    def __init__(self, button, position, size, font_size, view):
        self.position = position
        self.size = size
        self.font_size = font_size
        self.button = button
        self.view = view
    
    def contains(self, pos):
        return (
            pos[0] >= self.position[0] and
            pos[0] <= self.position[0] + self.size[0] and
            pos[1] >= self.position[1] and
            pos[1] <= self.position[1] + self.size[1]
        )

    def on_mouse_press(self, pos):
        if self.contains(pos):
            self.button.state = ButtonState.CLICKED
    
    def on_mouse_release(self, pos):
        if self.contains(pos):
            if self.button.state == ButtonState.CLICKED:
                self.button.callback()
            self.button.state = ButtonState.HOVERED
        else:
            self.button.state = ButtonState.NORMAL

    def on_mouse_move(self, pos):
        if self.contains(pos):
            if self.button.state != ButtonState.CLICKED:
                self.button.state = ButtonState.HOVERED
        else:
            self.button.state = ButtonState.NORMAL

    def draw(self, display):
        self.view.draw(display, self.position, self.size, self.font_size)
