from enum import Enum, auto

class InputState(Enum):
    NORMAL = auto()
    HOVERED = auto()
    CLICKED = auto()
    FOCUSED = auto()

class CommandsInput:
    NO_HIGHLIGHT = -1

    def __init__(self, enabled=True, focused=False):
        self.enabled = enabled
        self.commands = []
        self.highlight = CommandsInput.NO_HIGHLIGHT
        self.state = InputState.FOCUSED if focused else InputState.NORMAL
        self.hint = None
        self.hint_shown = 0
    
    def highlight_next(self):
        self.highlight = (self.highlight + 1) % len(self.commands)
    
    def no_highlight(self):
        self.highlight = CommandsInput.NO_HIGHLIGHT

    def next_hint(self):
        self.hint_shown += 1
        self.commands = self.hint[:self.hint_shown]
