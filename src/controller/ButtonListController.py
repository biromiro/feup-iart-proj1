from src.graphics.HeadingView import HeadingView
from src.model.Button import Button
from src.controller.ButtonController import ButtonController
from src.controller.Controller import Controller

class ButtonListController(Controller):
    def __init__(self, buttons, position, font_size, button_size, padding, view, back_action=None, title=None):
        self.position = position
        self.font_size = font_size
        self.width = button_size[0]
        x, y = position
        
        self.title = None
        if title:
            self.title = HeadingView(title)
            y += int(font_size*2)

        self.controllers = []
        if back_action:
            back_button = Button('Back', back_action)
            self.controllers += [ButtonController(back_button, (x, y), (int(button_size[0]*0.3), button_size[1]), font_size, view(back_button))]
            y += button_size[1] + padding

        self.controllers += [
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
        if self.title:
            self.title.draw(display, self.position, (self.width, int(self.font_size*1.5)))
        for controller in self.controllers:
            controller.draw(display)
