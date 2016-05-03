#Step 5
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
        self.moveToPlayer()
    def moveToPlayer(self):
        if player.x > self.x:
            self.moveRight()
        elif player.y > self.y:
            self.moveUp()
        elif player.x < self.x:
            self.moveLeft()
        elif player.y < self.y:
            self.moveDown()

monst = myMonster(1,1,'dog.png')
game.addGameObject(monst)

game.run()
