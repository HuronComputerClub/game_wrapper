#Step 8
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 2, 'cat.png')
game.addGameObject(player)

for x in range(5):
    game.placeWall(x+5, 5)
#Scope!
def distbtw(o1, o2):
    return abs(o1.x - o2.x) + abs(o1.y - o2.y)


class myMonster(Monster):
    def takeTurn(self):
        coins = game.getAllOfType(Coin)
        nearestCoin = coins[0]
        for coin in coins:
            dist = distbtw(coin, player)
            if dist < distbtw(nearestCoin, player):
                nearestCoin = coin
        self.moveToThing(nearestCoin)
    def moveToThing(self, thing):
        moved = False
        if thing.x > self.x:
            moved = self.moveRight()
            if not moved:
                moved = self.moveDown()
        if thing.x < self.x and not moved:
            moved = self.moveLeft()
            if not moved:
                moved = self.moveDown()  
        if thing.y > self.y and not moved:
            moved = self.moveUp()
            if not moved:
                moved = self.moveRight()            
        if thing.y < self.y and not moved:
            moved = self.moveDown()
            if not moved:
                moved = self.moveRight()            

    def distanceTo(self, thing):
        return abs(self.x - thing.x) + abs(self.y - thing.y)

monst = myMonster(1,1,'dog.png')
game.addGameObject(monst)

game.run()
