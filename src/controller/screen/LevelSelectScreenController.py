import pygame
from src.controller.ProblemLoader import ProblemLoader
from src.controller.ButtonGridController import ButtonGridController
from src.controller.screen.BoardScreenController import BoardScreenController
from src.graphics.BoardButtonView import BoardButtonView
from src.controller.Controller import Controller
from src.model.Button import Button

class LevelSelectScreenController(Controller):
    def __init__(self, push_screen, human_player, levels=None):
        if not levels:
            levels = ProblemLoader.load_all_files()
        
        self.levels = ButtonGridController(
            [Button(level, lambda level=level: push_screen(BoardScreenController, level, human_player)) for level in levels],
            (0, 0), 30, (256, 300), (64, 32), BoardButtonView, 2,
            title='Choose level:'
        )
    
    def on_mouse_press(self, pos):
        self.levels.on_mouse_press(pos)
    
    def on_mouse_release(self, pos):
        self.levels.on_mouse_release(pos)

    def on_mouse_move(self, pos):
        self.levels.on_mouse_move(pos)
    
    def draw(self, display):
        self.levels.draw(display)
