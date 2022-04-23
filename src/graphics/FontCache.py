import pygame

class FontCache:
    def __init__(self, system_font=False):
        self.cache = None
        self.name = None
        self.size = None
        self.sysfont = system_font
    
    def get(self, name, size):
        if self.name != name or self.size != size:
            self.name = name
            self.size = size
            self.cache = pygame.font.SysFont(name, size) if self.sysfont else pygame.font.Font(name, size)
        return self.cache
