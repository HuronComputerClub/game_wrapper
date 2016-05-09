import sys, pygame, os, random, time, math
from graphics import *
from pygame.locals import *

KEYS={"UP":273,"RIGHT":275,"DOWN":274,"LEFT":276}


def distance(p0, p1):
    return math.sqrt((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)

def gridDistance(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1])
        
class VisualEffect:
    def __init__(self, imagePath, turnsLeft=1):
        self.imagePath=imagePath
        self.turnsLeft=turnsLeft       

class GameController:
    textHeight = 75
    
    def __init__(self, boardWidth=25, boardHeight=20, tileSize = 32):
        pygame.init()
        
        self.boardWidth=boardWidth
        self.boardHeight=boardHeight
        self.stickerBoard=[[-1 for y in range(0, boardHeight)] for x in xrange(0, boardWidth)]
        self.effects=[]
        self.backgroundImage=0
        self.errorImage=0
        self.graphics=GraphicsController(gameWidth  = boardWidth*tileSize,
                                         gameHeight = boardHeight*tileSize,
                                         tileWidth  = tileSize,
                                         tileHeight = tileSize,
                                         textHeight = GameController.textHeight)
        self.objects=[]
        self.imageDict={}
        self.tileSize=tileSize
        self.loadImages()
        self.player=None
        self.currentMessage = ""

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
        self.graphics.drawBorders()

    def spriteIndexFromName(self, imageName):
        return self.imageDict.get(imageName, self.errorImage)

    def setBackgroundImage(self, imageName):
        self.backgroundImage=self.spriteIndexFromName(imageName)

    def addGameObject(self, gameObject):
        self.objects.append(gameObject)
        gameObject.spriteIndex=self.spriteIndexFromName(gameObject.spriteName)
        gameObject.controller=self

        if(isinstance(gameObject, Player) and self.player == None):
            self.player = gameObject

    def run(self):
        """handle events as a loop"""
        def nextObj(obj_num, obj_list):
            return (obj_num+1)%len(obj_list)
        run=True
        self.drawMap()
        objectTurn=0
        while run==True:
            currentObject=self.objects[objectTurn]  #The object whose turn it is
            while isinstance(currentObject, Wall): #skip over walls
                objectTurn=nextObj(objectTurn,self.objects)
                currentObject=self.objects[objectTurn]
            for e in pygame.event.get():            #Handle events
                if e.type==pygame.QUIT:
                    run=False
                if isinstance(currentObject, Player): #It is the player's turn
                    if currentObject.tryTurn(e):    #The player trys to move with the event
                        objectTurn=nextObj(objectTurn,self.objects)                       
            if isinstance(currentObject, Monster):  #It is a monster's turn
                currentObject.takeTurn()
                time.sleep(0.1)
                objectTurn=nextObj(objectTurn,self.objects) 
            elif not isinstance(currentObject, Player): #It is not a player or a monster's turn, it is likely scenery or an object's turn
                currentObject.takeTurn()
                objectTurn=nextObj(objectTurn,self.objects) 
            if(player):
                self.graphics.drawScoreBoard(self.currentMessage, "Score: " + str(self.player.score))
            else:
                self.graphics.drawScoreBoard(self.currentMessage, "")

            self.drawMap()
            pygame.display.flip()
        pygame.quit()

    def getTileOfScreenPosition(self, pos):
        tileX=pos[0]/self.tileSize
        tileY=(self.graphics.screenHeight - pos[1])/self.tileSize
        return (tileX, tileY)

    def getPlayerLoc(self):
        for obj in self.objects:
            if isinstance(obj, Player):
                return (obj.x, obj.y)

    def spaceHasObject(self, x, y):
        for obj in self.objects:
            if obj.x==x and obj.y==y:
                return True
        return False

    def spaceHasObjective(self, x, y):  #Checks if there is anything in a space
        for obj in self.objects:
            if obj.x==x and obj.y==y and isinstance(obj, Objective):
                return True
        return False

    def spaceIsFull(self, x, y):        #Checks if there is an object that a monster can't move over
        return self.spaceHasObject(x, y) and not self.spaceHasObjective(x, y)
        

    def playerTouchObjective(self, x, y):
        for obj in self.objects:
            if obj.x==x and obj.y==y and isinstance(obj, Objective):
                obj.onPlayerTouch()

    def placeWall(self, x, y):
        if not self.spaceHasObject(x, y):
            theWall=Wall(x, y, 'wall.png')
            self.addGameObject(theWall)

    def playerScorePoints(self, numPoints):
        self.player.score += numPoints

    def removeObject(self, theObject):
        for obj in self.objects:
            if obj == theObject:
                self.objects.remove(obj)

    def getAllOfType(self, typeName):
        elements = []
        for obj in self.objects:
            if isinstance(obj, typeName):
                elements.append(obj)
        return elements

    def log(self, text):
        self.currentMessage = text
        
class GameObject(object): #The class that ingame objects inherit from
    def __init__(self, x, y, spriteName):
        self.x=x
        self.y=y
        self.spriteName=spriteName
        self.spriteIndex=None

    def takeTurn(self):
        pass

    def moveUp(self):
        if not self.controller.spaceIsFull(self.x, self.y + 1):
            self.y += 1
        
    def moveDown(self):
        if not self.controller.spaceIsFull(self.x, self.y - 1):
            self.y -= 1

    def moveLeft(self):
        if not self.controller.spaceIsFull(self.x - 1, self.y):
            self.x -= 1

    def moveRight(self):
        if not self.controller.spaceIsFull(self.x + 1, self.y):
            self.x += 1

    def getClosestOfType(self, typeName):
        candidates = self.controller.getAllOfType(typeName)
        minDist = 100000
        closest = None
        for el in candidates:
            if(el == self):
                continue
            thisDist = gridDistance((el.x, el.y), (self.x, self.y))
            if thisDist < minDist:
                minDist = thisDist
                closest = el
        return closest

class Monster(GameObject):
    def __init__(self, x, y, spriteName):
        super(Monster, self).__init__(x, y, spriteName)
        self.speed=2
    
    def takeTurn(self, event):
        pass

    #Return values:
    #0 means monster made it to the goal
    #1 means monster moved towards the goal
    #2 means monster is stuck next to the goal
    #3 means monster is stuck away from the goal
    def moveTowardsSpace(self, x, y, moves):
        currentPos=(self.x, self.y)
        goal=(x, y)
        while moves>0:
            #possibleMoves=((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)) #Allows Diagonal moves
            possibleMoves=((1, 0), (0, 1), (-1, 0), (0, -1))
            bestDist=distance(currentPos, goal)
            bestMove=(0, 0)
            for move in possibleMoves:
                newPos=[currentPos[0]+move[0], currentPos[1]+move[1]]
                if not self.controller.spaceIsFull(newPos[0], newPos[1]):
                    dist=distance(newPos, goal)
                    if dist<bestDist:
                        bestDist=dist
                        bestMove=move
            if bestMove!=(0, 0):
                self.x+=bestMove[0]
                self.y+=bestMove[1]
                currentPos=(self.x, self.y)
                moves-=1
            else:
                if bestDist==0:
                    return 0
                if bestDist<2:
                    return 2
                if bestDist>=2:
                    return 3
        return 1

    def moveTowardsPlayer(self):
        thePlayer = self.controller.player
        xGoal = thePlayer.x
        yGoal = thePlayer.y
        self.moveTowardsSpace(xGoal, yGoal, 1)

class Objective(GameObject):
    def onPlayerTouch(self):
        pass

class Wall(GameObject):
    pass

class Coin(Objective):
    
    def __init__(self, x, y, spriteName = 'coin.png'):
        self.x = x
        self.y = y
        self.spriteName = spriteName
        self.spriteIndex = None
    
    def onPlayerTouch(self):
        self.controller.playerScorePoints(1)
        

        xPlace = random.randint(0, self.controller.boardWidth - 1)
        yPlace = random.randint(0, self.controller.boardHeight - 1)
        placeAttempts = 0

        while(placeAttempts < 50):
            if(not self.controller.spaceHasObject(xPlace, yPlace)): #Found an open space, moving coin to it
                self.x = xPlace
                self.y = yPlace
                break
            
            xPlace = random.randint(0, self.controller.boardWidth - 1) #Didn't find an open space
            yPlace = random.randint(0, self.controller.boardHeight - 1)
            placeAttempts += 1
            if(placeAttempts == 50):
                print "Failed coin placement attempt"
                self.controller.removeObject(self)  #Delete the coin

class Player(GameObject):
    def __init__(self, x, y, spriteName):
        super(Player, self).__init__(x, y, spriteName)
        self.speed=2
        self.score=0
        
    def mouse(self, event):
        return self.controller.getTileOfScreenPosition(event.pos)[0], self.controller.getTileOfScreenPosition(event.pos)[1]
    def tryTurn(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN:
            return self.takeTurn(event)
        return False
    def takeTurn(self, event):
        moved = False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1: #register only Left clicks
            x, y = self.mouse(event)
            if not self.controller.spaceIsFull(x,y) and (abs(self.x-x)+abs(self.y-y)==1):
                self.x = x
                self.y = y
                moved = True
                
        elif event.type==pygame.KEYDOWN:
            x=self.x
            y=self.y
            
            if event.key == KEYS["RIGHT"]:
                x += 1
            elif event.key == KEYS["LEFT"]:
                x -= 1
            elif event.key == KEYS["DOWN"]:
                y -= 1
            elif event.key == KEYS["UP"]:
                y += 1
            else:
                moved = False
            if not self.controller.spaceIsFull(x,y):
                self.x=x
                self.y=y
                moved = True

        if moved and (not self.controller.spaceIsFull(x,y)):
            self.controller.playerTouchObjective(x, y)

        return moved
        
game = GameController(20,20,35)
game.setBackgroundImage('caveTile.png')

theCoin = Coin(10, 10)
game.addGameObject(theCoin)

player = game.player
