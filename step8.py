#Step 8
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

#Scope!
def distbtw(o1, o2):
    return abs(o1x-o2x) + abs(01y-02y)


class myMonster(Monster):
    def takeTurn(self):
        coins = getall("Coin")
        nearestcoin = coins[0]
        for coin in coins:
            dist = distbtw(coin, Player):
            if dist < distbtw(nearestcoin, Player):
                nearestcoin = coin
        movetothing(nearestcoin)
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
