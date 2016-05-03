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
    game.placeWall(x+5, 5)

class myMonster(Monster):
    def takeTurn(self):
        myCoin = self.getClosestOfType(Coin)
        if self.distanceTo(myCoin) < self.distanceTo(player):
            self.moveToThing(myCoin)
        else:
            self.moveToThing(player)
    def moveToThing(self, thing):
        if thing.x > self.x:
            self.moveRight()
        elif thing.y > self.y:
            self.moveUp()
        elif thing.x < self.x:
            self.moveLeft()
        elif thing.y < self.y:
            self.moveDown()
    def distanceTo(self, thing):
        return abs(self.x - thing.x) + abs(self.y - thing.y)

monst = myMonster(1,1,'dog.png')
game.addGameObject(monst)

game.run()
