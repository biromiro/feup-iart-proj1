from src.ButtonController import ButtonController
from src.Controller import Controller

class ButtonListController(Controller):
    def __init__(self, buttons, position, font_size, button_size, padding, view):
        x, y = position
        
        self.controllers = [
            ButtonController(button, (x, y + idx*(button_size[1] + padding)), button_size, font_size, view(button)) 
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
        for controller in self.controllers:
            controller.draw(display)
