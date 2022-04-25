import pygame
from src.controller.screen.MainMenuScreenController import MainMenuScreenController
from src.graphics.Color import Color
import sys

pygame.init()
pygame.font.init()

class Application:
    def __init__(self):
        self.framerate = 60
        self.width = 1024
        self.height = 720
        self.screen_stack = []
        self.push_screen(MainMenuScreenController)
    
    def run(self):
        display = pygame.display.set_mode((self.width, self.height))
        
        clock = pygame.time.Clock()
        timepassed = 0
        while True:
            self.handle_events()
            self.screen_stack[-1].update(timepassed)
            self.draw(display)
            timepassed = clock.tick(self.framerate)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pop_screen()
                else:
                    self.screen_stack[-1].on_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.screen_stack[-1].on_mouse_press(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.screen_stack[-1].on_mouse_release(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.screen_stack[-1].on_mouse_move(event.pos)
    
    def draw(self, display):
        display.fill(Color.WHITE)
        self.screen_stack[-1].draw(display)
        pygame.display.flip()

    def push_screen(self, controller, *args, **kwargs):
        self.screen_stack.append(controller(self.push_screen, *args, **kwargs))

    def pop_screen(self):
        if len(self.screen_stack) > 1:
            self.screen_stack.pop()
