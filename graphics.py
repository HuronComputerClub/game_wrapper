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
    def __init__(self, gameWidth, gameHeight, tileWidth, tileHeight, textHeight):
        self.screenWidth = gameWidth
        self.screenHeight = gameHeight + textHeight
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.textHeight = textHeight
        
        self.sprites = []
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.RESIZABLE)

    def drawTile(self, x, y, spriteIndex):
        drawLoc=(x*self.tileWidth, self.screenHeight - self.tileHeight - y*self.tileHeight)
        self.screen.blit(self.sprites[spriteIndex], drawLoc)

    def drawBorders(self):
        for xDiv in range(1, self.screenWidth / self.tileWidth):
            pygame.draw.line(self.screen, BLACK, (xDiv * self.tileWidth, self.textHeight), (xDiv * self.tileWidth, self.screenHeight))

        for yDiv in range(1, (self.screenHeight - self.textHeight) / self.tileHeight):
            pygame.draw.line(self.screen, BLACK, (0, self.screenHeight - yDiv * self.tileHeight), (self.screenWidth, self.screenHeight - yDiv * self.tileHeight))

    def drawScoreBoard(self, textLeft, textRight):
        self.screen.fill(BLACK, (0, 0, self.screenWidth, self.textHeight))
        
        font = pygame.font.Font(None, 45)
        leftTextRender = font.render(textLeft, True, WHITE)
        leftTextPos = leftTextRender.get_rect()
	leftTextPos.left = 25
	leftTextPos.centery = self.textHeight / 2

	rightTextRender = font.render(textRight, True, WHITE)
	rightTextPos = rightTextRender.get_rect()
	rightTextPos.right = self.screenWidth - 25
	rightTextPos.centery = self.textHeight / 2
	
	self.screen.blit(leftTextRender, leftTextPos)
        self.screen.blit(rightTextRender, rightTextPos)
