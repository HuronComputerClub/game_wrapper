import pygame
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print 'Cannot load image:', name
        return None
    image = image.convert()

    corner = image.get_at((0,0)) #color at top left corner
    if colorkey is None and (corner==BLACK or corner==WHITE):
        #no color specified - only make black or white -> transparent
        colorkey = corner
    image.set_colorkey(colorkey, RLEACCEL)
    return image

class GraphicsController:       
    def __init__(self, screenWidth, screenHeight, tileWidth, tileHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        
        self.sprites=[]
        self.screen=pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.RESIZABLE)

    def drawTile(self, x, y, spriteIndex):
        drawLoc=(x*self.tileWidth, self.screenHeight - self.tileHeight - y*self.tileHeight)
        self.screen.blit(self.sprites[spriteIndex], drawLoc)

    def drawBorders(self):
        for xDiv in range(self.screenWidth / self.tileWidth):
            pygame.draw.line(self.screen, BLACK, ((xDiv+1)*self.tileWidth, 0), ((xDiv+1)*self.tileWidth, self.screenHeight))

        for yDiv in range(self.screenHeight / self.tileHeight):
            pygame.draw.line(self.screen, BLACK, (0, (yDiv+1)*self.tileHeight), (self.screenWidth, (yDiv+1)*self.tileHeight))
            
