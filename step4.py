#Step 4
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 2, 'cat.png')
game.addGameObject(player)

for x in range(5):
    game.placeWall(x+4, 5)
    pass

class myMonster(Monster):
    def takeTurn(self):
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
