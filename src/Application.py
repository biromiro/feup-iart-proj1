import pygame
from src.ScreenController import ScreenController
import src.graphics # initializes pygame
from src.graphics.Color import Color
import sys

class Application:
    def __init__(self):
        self.framerate = 60
        self.width = 1024
        self.height = 720
        self.controller = ScreenController()
    
    def run(self):
        display = pygame.display.set_mode((self.width, self.height))
        
        clock = pygame.time.Clock()
        timepassed = 0
        while True:
            self.handle_events()
            self.controller.update(timepassed)
            self.draw(display)
            timepassed = clock.tick(self.framerate)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:
                self.controller.on_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.controller.on_mouse_press(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.controller.on_mouse_release(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.controller.on_mouse_move(event.pos)
    
    def draw(self, display):
        display.fill(Color.WHITE)
        self.controller.draw(display)
        pygame.display.flip()
