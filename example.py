#Example of the use of the game structure file
import pygame

from gameFile import *

class myMonster(Monster):
    def takeTurn(self): #Example chasing monster
        playerLoc=self.controller.getPlayerLoc()
        if self.x<playerLoc[0]:
            if not self.controller.checkSpace(self.x+1, self.y):
                self.x+=1
        if self.x>playerLoc[0]:
            if not self.controller.checkSpace(self.x-1, self.y):
                self.x-=1
        if self.y<playerLoc[1]:
            if not self.controller.checkSpace(self.x, self.y+1):
                self.y+=1
        if self.y>playerLoc[1]:
            if not self.controller.checkSpace(self.x, self.y-1):
                self.y-=1
            
game = GameController(20,20,35)
game.setBackgroundImage('borderTile.png')

#create an instance of your modified monster
character = myMonster(1, 1, 'circle.png')
dog = myMonster(1, 3, 'dog.png')

game.addGameObject(character)
game.addGameObject(dog)

#create a player character
player = Player(1, 2, 'cat.png')
game.addGameObject(player)

game.run()
