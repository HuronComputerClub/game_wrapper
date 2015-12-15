import sys, pygame, os
pygame.init()

windowWidth=640
windowHeight=800

imageHeight=128
imageWidth=128

screen=pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
sprites=[]

for i in xrange(0, 1):
    imageLocations=[]
    for root, dirs, files in os.walk('images'):
        for fileName in files:
            imagePath=os.path.join(root, fileName)
            imageLocations.append(imagePath)

    for imagePath in imageLocations:
        image=pygame.image.load(imagePath)
        image=pygame.transform.smoothscale(image,(imageWidth, imageHeight))
        sprites.append(image)

    for index in xrange(0, len(sprites)):
        screen.blit(sprites[index], (imageWidth*index, imageWidth*0))

class graphicsController:
    sprites=[]
    screen
    
    screenWidth=800
    screenHeight=640
    tileWidth=64
    tileHeight=64
        
    def __init__(self, imagePath=None):
        screen=pygame.display.set_mode((screenWidth, screenHeight), )
        if imagePath is not None:
            loadImagesFromDirectory(sprites, imagePath) 
        
    def loadImagesFromDirectory(spriteLoc, path): #Maybe load images should return sprite list instead?
        for root, dirs, files in os.walk(path):
            for fileName in files:
                imagePath=os.path.join(root, fileName)
                imageLocations.append(imagePath)

        for imagePath in imageLocations:
            image=pygame.image.load(imagePath)
            image=pygame.transform.smoothscale(image,(imageWidth, imageHeight))
            spriteLoc.append(image)

    def drawTile(x, y, spriteIndex):
        drawLoc=(x*tileWidth, y*tileHeight)
        screen.blit(sprites[spriteIndex], drawLoc)

class gameController:
    pass
    #objects

class gameObject:
    data={}
    def __init__(self, x, y, spriteIndex):
        data['xPos']=x
        data['yPos']=y
        data['spriteIndex']=spriteIndex

class moster:
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
