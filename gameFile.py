import sys, pygame, os, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)


def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print 'Cannot load image:', name
        return None
    image = image.convert()

    corner = image.get_at((0,0)) #color at top left corner
    if colorkey is None and (corner==BLACK or corner==WHITE):
        #no color specified. Corner is black or white
        colorkey = corner
    image.set_colorkey(colorkey, RLEACCEL)
    return image

class graphicsController:
    screenWidth=800
    screenHeight=640
    tileWidth=32
    tileHeight=32
        
    def __init__(self, imagePath=None):
        self.sprites=[]
        self.screen=pygame.display.set_mode((graphicsController.screenWidth, graphicsController.screenHeight), pygame.RESIZABLE)
        if imagePath is not None:
            self.loadImages()

    def drawTile(self, x, y, spriteIndex):
        drawLoc=(x*graphicsController.tileWidth, y*graphicsController.tileHeight)
        self.screen.blit(self.sprites[spriteIndex], drawLoc)

    def drawGrid(self, drawlist):        
        for x in xrange(0,len(drawlist)):
            col = drawlist[x]
            for y in range(0,len(row)):
                drawTile(x,y,col[y])
        
class visualEffect:
    def __init__(self, imagePath, turnsLeft=1):
        self.imagePath=imagePath
        self.turnsLeft=turnsLeft
        

class gameController:
    def __init__(self, boardWidth=25, boardHeight=20):
        pygame.init()
        
        self.boardWidth=boardWidth
        self.boardHeight=boardHeight
        self.stickerBoard=[[-1 for y in range(0, boardHeight)] for x in xrange(0, boardWidth)]
        self.effects=[]
        self.backgroundImage=0
        self.errorImage=0
        self.graphics=graphicsController()
        self.objects=[]
        self.imageDict={}

    def turn(self):
        for gameObject in self.objects:
            gameObject.onTurn()   

    def loadImages(self): #Loads all of the image files in the images folder into the game
        imageLocations=[]
        for root, dirs, files in os.walk('images'):
            for fileName in files:
                imagePath=os.path.join(root, fileName)
                imageLocations.append(imagePath)
                image=load_image(imagePath)
                if image!=None:
                    image=pygame.transform.smoothscale(image, (self.graphics.tileWidth, self.graphics.tileHeight))
                    self.graphics.sprites.append(image)
                    imageIndex=len(self.graphics.sprites)-1
                    self.imageDict[fileName]=imageIndex
                    if fileName=='error.png':
                        self.errorImage=imageIndex

    def drawMap(self):
        for y in xrange(0, self.boardHeight):
            for x in xrange(0, self.boardWidth):
                self.graphics.drawTile(x, y, self.backgroundImage) #Draws background tiles first
                for gameObject in self.objects:                    #Then draws gameobjects on top
                    if gameObject.x==x and gameObject.y==y:
                        self.graphics.drawTile(x, y, gameObject.spriteIndex)
                for effect in self.effects:                        #Then draws effects on top of that
                    if effect.x==x and effect.y==y:
                        self.graphics.drawTile(x, y, effect.spriteIndex)

    def spriteIndexFromName(self, imageName):
        return self.imageDict.get(imageName, self.errorImage)

    def setBackgroundImage(self, imageName):
        self.backgroundImage=self.spriteIndexFromName(imageName)

    def addGameObject(self, gameObject):
        self.objects.append(gameObject)
        gameObject.spriteIndex=self.spriteIndexFromName(gameObject.spriteName)

    def run(self):
        """handle events as a loop"""
        run=True
        while run==True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    run=False
                if e.type==pygame.KEYDOWN:               
                    self.turn()
                    self.drawMap()
            pygame.display.flip()
    
        pygame.quit()

        
class gameObject:                               #The class that ingame objects inherit from
    def __init__(self, x, y, spriteName):
        self.x=x
        self.y=y
        self.spriteName=spriteName
        self.spriteIndex=None

    def onTurn(self):
        pass


class monster(gameObject):
    def onTurn(self):
        direction=random.randint(1, 4)
        if direction==1: #move left
            if self.x>1:
                self.x-=1
            
        if direction==2: #move up
            if self.y<19:
                self.y+=1

        if direction==3: #move right
            if self.x<24:
                self.x+=1

        if direction==4: #move down
            if self.y>0:
                self.y-=1

class player(gameObject):
    pass
