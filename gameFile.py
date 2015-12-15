import sys, pygame, os
from pygame.locals import *
pygame.init()

windowWidth=640
windowHeight=800

imageHeight=128
imageWidth=128

screen=pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
sprites=[]

def load_image(name, colorkey=None):
    fullname = name#os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

screen.fill((20,20,20))
for i in xrange(0, 1):
    imageLocations=[]
    for root, dirs, files in os.walk('images'):
        for fileName in files:
            imagePath=os.path.join(root, fileName)
            imageLocations.append(imagePath)

    for imagePath in imageLocations:
        image=load_image(imagePath, -1)
        image=pygame.transform.smoothscale(image,(imageWidth, imageHeight))
        sprites.append(image)

    for index in xrange(0, len(sprites)):
        screen.blit(sprites[index], (imageWidth*index, imageWidth*0))

class graphicsController:
    screenWidth=800
    screenHeight=640
    tileWidth=64
    tileHeight=64
        
    def __init__(self, imagePath=None):
        self.sprites=[]
        self.screen=pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        if imagePath is not None:
            self.loadImages()
        
    def loadImages(self):
        for imagePath in imageLocations:
            image=load_image(imagePath)
            image=pygame.transform.smoothscale(image,(imageWidth, imageHeight))
            self.sprites.append(image)

    def drawTile(self, x, y, spriteIndex):
        drawLoc=(x*tileWidth, y*tileHeight)
        screen.blit(sprites[spriteIndex], drawLoc)

    def drawGrid(self, drawlist):
        for x in xrange(0,len(drawlist)):
            row = drawlist[x]
            for y in range(0,len(row)):
                drawTile(x,y,row[y])

class gameController:
    pass
    #objects

class gameObject:
    data={}
    def __init__(self, x, y, spriteIndex):
        data['xPos']=x
        data['yPos']=y
        data['spriteIndex']=spriteIndex

class monster:
    pass

class player:
    pass
run=True
while run==True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=False
    pygame.display.flip()
    
pygame.quit()
