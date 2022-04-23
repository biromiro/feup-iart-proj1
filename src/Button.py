from enum import Enum, auto

class ButtonState(Enum):
    NORMAL = auto()
    HOVERED = auto()
    CLICKED = auto()

class Button:
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback
        self.state = ButtonState.NORMAL
