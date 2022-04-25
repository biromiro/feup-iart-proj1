import pygame

class RobotView:
    SPRITE = pygame.image.load('resources/images/robot.png')
    
    def draw(self, display, position, size):
        width, height = size
        width_bound = int(height * self.SPRITE.get_width() / self.SPRITE.get_height())
        if width_bound <= width:
            width = width_bound
        else:
            height = int(width * self.SPRITE.get_height() / self.SPRITE.get_width())

        sprite = pygame.transform.scale(RobotView.SPRITE, (width, height))
        display.blit(sprite, sprite.get_rect(center=position))
        
