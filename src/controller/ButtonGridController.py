from src.graphics.HeadingView import HeadingView
from src.controller.ButtonController import ButtonController
from src.controller.Controller import Controller
import math

class ButtonGridController(Controller):
    def __init__(self, buttons, position, font_size, button_size, padding, view, num_rows, title=None):
        self.position = position
        self.font_size = font_size
        x, y = position
        px, py = padding
        
        self.title = None
        if title:
            self.title = HeadingView(title)
            y += int(font_size*2)

        num_cols = math.ceil(len(buttons)/num_rows)
        self.width = (button_size[0] + px)*num_cols + px

        self.controllers = [
            ButtonController(button, (x + px + idx//num_rows*(button_size[0] + px), y + idx%num_rows*(button_size[1] + py)), button_size, font_size, view(button)) 
            for idx, button in enumerate(buttons)
        ]
        
    def on_mouse_press(self, pos):
        for controller in self.controllers:
            controller.on_mouse_press(pos)
    
    def on_mouse_release(self, pos):
        for controller in self.controllers:
            controller.on_mouse_release(pos)

    def on_mouse_move(self, pos):
        for controller in self.controllers:
            controller.on_mouse_move(pos)

    def draw(self, display):
        if self.title:
            self.title.draw(display, self.position, (self.width, int(self.font_size*1.5)))
        for controller in self.controllers:
            controller.draw(display)
