from src.graphics.FontCache import FontCache
from src.graphics.Color import Color
from src.graphics.RobotView import RobotView

class TitleView:
    FONT_NAME = ['segoeui', 'helvetica', 'arial']
    COLOR = Color.BLACK
    FONT = FontCache(system_font=True)
    ROBOT_SIZE = (200, 200)
    
    def draw(self, display, position):
        x, y = position
        width, height = TitleView.ROBOT_SIZE

        font_height = int(height*0.4)
        font = TitleView.FONT.get(TitleView.FONT_NAME, font_height)
        font.set_bold(True)

        font_width = font.size('R O B O T')[0]

        RobotView().draw(display, (x-(font_width+width//2)//2, y), (width, height))
        
        for idx, text in enumerate(['R O B O T', 'M A Z E S']):
            text = font.render(text, True, TitleView.COLOR)
            display.blit(text, text.get_rect(midtop=(x + width//4, y + 5*font.get_descent() + idx*font_height)))
