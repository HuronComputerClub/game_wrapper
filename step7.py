#Step 7
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 2, 'cat.png')
game.addGameObject(player)

for x in range(10):
    #put walls down at (x,y)
    pass

class myMonster(Monster):
    def takeTurn(self):
        mycoin = game.getclosest("Coin")
        if distanceTo(myCoin) < distanceTo(Player):
            movetothing(mycoin)
        else:
            movetothing(Player)
    def movetothing(self):
        if thingx > myx:
            moveright
        elif thingy > myy:
            moveup
        elif thingx < myx:
            moveleft
        elif thingy < myy:
            movedown
    def distanceTo(self, thing):
        return abs(myx-thingx) + abs(myy-thingy)

monst = myMonster(1,1,'dog.png')
game.addGameObject(monst)

game.run()
