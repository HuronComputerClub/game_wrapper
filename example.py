#Step 8
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 5, 'cat.png')
game.addGameObject(player)

for x in range(5):
    game.placeWall(x+5, 5)
for y in range(10):
	game.placeWall(5,y)
	game.placeWall(10,y+5)
newCoin = Coin(1,1)
game.tryToRandomlyPlaceObject(newCoin)
game.addGameObject(newCoin)
#Scope!
def distbtw(o1, o2):
    return abs(o1.x - o2.x) + abs(o1.y - o2.y)


class myMonster(Monster):
    def takeTurn(self):
        coins = game.getAllOfType(Coin)
        nearestCoin = coins[0]
        for coin in coins:
            dist = distbtw(coin, player)
            if dist < distbtw(nearestCoin, self):
                nearestCoin = coin
        self.moveToThing(nearestCoin)
    def moveToThing(self, thing):
        moved = False
        if thing.x > self.x:
            if not game.spaceIsFull(self.x+1,self.y):
            	moved = self.moveRight()
            elif thing.y>self.y and not game.spaceIsFull(self.x+1,self.y+1):
            	moved = self.moveUp()
            elif thing.y < self.y and not game.spaceIsFull(self.x+1,self.y-1):
            	moved = self.moveDown()
        if thing.x < self.x and not moved:
            if not game.spaceIsFull(self.x-1,self.y):
            	moved = self.moveLeft()
            elif thing.y > self.y and not game.spaceIsFull(self.x-1,self.y+1):
            	moved = self.moveUp()
            elif thing.y < self.y and not game.spaceIsFull(self.x-1,self.y-1):
            	moved = self.moveDown()

        if thing.y > self.y and not moved:
            if not game.spaceIsFull(self.x,self.y+1):
            	moved = self.moveUp()
            elif thing.x>self.x and not game.spaceIsFull(self.x+1,self.y+1):
            	moved = self.moveRight()
            elif thing.x < self.x and not game.spaceIsFull(self.x-1,self.y+1):
            	moved = self.moveLeft()
        if thing.y < self.y and not moved:
            if not game.spaceIsFull(self.x,self.y-1):
            	moved = self.moveDown()
            elif thing.x > self.x and not game.spaceIsFull(self.x+1,self.y-1):
            	moved = self.moveRight()
            elif thing.x < self.x and not game.spaceIsFull(self.x-1,self.y-1):
            	moved = self.moveLeft()

    def distanceTo(self, thing):
        return abs(self.x - thing.x) + abs(self.y - thing.y)

monst = myMonster(1,1,'dog.png')
game.addGameObject(monst)

game.run()
