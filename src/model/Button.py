from enum import Enum, auto

class ButtonState(Enum):
    NORMAL = auto()
    HOVERED = auto()
    CLICKED = auto()

class Button:
    """Represents a UI button."""
    def __init__(self, data, callback):
        self.data = data
        self.callback = callback
        self.state = ButtonState.NORMAL
