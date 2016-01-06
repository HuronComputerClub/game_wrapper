import sys, pygame, os, random, time
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

KEYS={"UP":273,"RIGHT":275,"DOWN":274,"LEFT":276}


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
        drawLoc=(x*self.tileWidth, y*self.tileHeight)
        self.screen.blit(self.sprites[spriteIndex], drawLoc)

    def drawGrid(self, drawlist):        
        for x in xrange(0,len(drawlist)):
            col = drawlist[x]
            for y in range(0,len(row)):
                drawTile(x,y,col[y])
        
class VisualEffect:
    def __init__(self, imagePath, turnsLeft=1):
        self.imagePath=imagePath
        self.turnsLeft=turnsLeft
        

class GameController:
    def __init__(self, boardWidth=25, boardHeight=20, tileSize = 32):
        pygame.init()
        
        self.boardWidth=boardWidth
        self.boardHeight=boardHeight
        self.stickerBoard=[[-1 for y in range(0, boardHeight)] for x in xrange(0, boardWidth)]
        self.effects=[]
        self.backgroundImage=0
        self.errorImage=0
        self.graphics=GraphicsController(screenWidth = boardWidth*tileSize,
                                         screenHeight = boardHeight*tileSize,
                                         tileWidth = tileSize, tileHeight = tileSize)
        self.objects=[]
        self.imageDict={}
        self.tileSize=tileSize
        self.loadImages()
        self.player=None  

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
                for GameObject in self.objects:                    #Then draws gameobjects on top
                    if GameObject.x==x and GameObject.y==y:
                        self.graphics.drawTile(x, y, GameObject.spriteIndex)
                for effect in self.effects:                        #Then draws effects on top of that
                    if effect.x==x and effect.y==y:
                        self.graphics.drawTile(x, y, effect.spriteIndex)

    def spriteIndexFromName(self, imageName):
        return self.imageDict.get(imageName, self.errorImage)

    def setBackgroundImage(self, imageName):
        self.backgroundImage=self.spriteIndexFromName(imageName)

    def addGameObject(self, GameObject):
        self.objects.append(GameObject)
        GameObject.spriteIndex=self.spriteIndexFromName(GameObject.spriteName)
        GameObject.controller=self

    def run(self):
        """handle events as a loop"""
        run=True
        self.drawMap()
        objectTurn=0
        while run==True:
            currentObject=self.objects[objectTurn] #The object whose turn it is
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    run=False
                if isinstance(currentObject, Player):
                    if currentObject.tryTurn(e): #The player gets the event and uses it to try to move.
                        objectTurn=(objectTurn+1)%len(self.objects)                       
            if isinstance(currentObject, Monster):
                currentObject.takeTurn()
                time.sleep(.5)
                objectTurn=(objectTurn+1)%len(self.objects)
            elif not isinstance(currentObject, Player): #currentObject is not a player or a monster. It is likely scenery or an objective.
                currentObject.takeTurn()
                objectTurn=(objectTurn+1)%len(self.objects)
            self.drawMap()
            pygame.display.flip()
        pygame.quit()

    def getTile(self, pos):
        tileX=pos[0]/self.tileSize
        tileY=pos[1]/self.tileSize
        return (tileX, tileY)

    def getPlayerLoc(self):
        for obj in self.objects:
            if isinstance(obj, Player):
                return (obj.x, obj.y)

    def checkSpace(self, x, y):
        for obj in self.objects:
            if obj.x==x and obj.y==y:
                return True
        return False
        
class GameObject: #The class that ingame objects inherit from
    def __init__(self, x, y, spriteName):
        self.x=x
        self.y=y
        self.spriteName=spriteName
        self.spriteIndex=None

    def takeTurn(self, event):
        pass

class Monster(GameObject):
    def takeTurn(self, event):
        pass

class Player(GameObject):
    def __init__(self, x, y, spriteName):
        self.x=x
        self.y=y
        self.spriteName=spriteName
        self.spriteIndex=None
        self.speed=2
    def mouse(self, event):
        return self.controller.getTile(event.pos)[0],self.controller.getTile(event.pos)[1]
    def tryTurn(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN or \
           event.type==pygame.KEYDOWN:
            return self.takeTurn(event)
        return False
    def takeTurn(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y = self.mouse(event)
            if self.controller.checkSpace(x,y):
                return False #the player cannot move here
            self.x = x
            self.y = y
            return True
