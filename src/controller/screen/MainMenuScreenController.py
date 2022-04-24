import pygame
from src.controller.ButtonListController import ButtonListController
from src.graphics.ButtonView import ButtonView
from src.controller.Controller import Controller
from src.model.Button import Button
from src.controller.screen.LevelSelectScreenController import LevelSelectScreenController
from src.graphics.TitleView import TitleView

class MainMenuScreenController(Controller):
    def __init__(self, push_screen):
        self.title = TitleView()
        self.buttons = ButtonListController(
            [
                Button('Play', lambda: push_screen(LevelSelectScreenController, True)),
                Button('AI', lambda: push_screen(LevelSelectScreenController, False)),
            ], 
            (350, 400), 30, (300, 50), 32, ButtonView,
        )
    
    def on_mouse_press(self, pos):
        self.buttons.on_mouse_press(pos)
    
    def on_mouse_release(self, pos):
        self.buttons.on_mouse_release(pos)

    def on_mouse_move(self, pos):
        self.buttons.on_mouse_move(pos)

    def draw(self, display):
        self.title.draw(display, (512, 200))
        self.buttons.draw(display)
