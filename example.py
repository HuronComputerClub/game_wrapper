#Example of the use of the game structure file
import pygame

from gameFile import *

class myMonster(Monster):
    def onTurn(self, event = None):
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["RIGHT"]:
                self.x += 1
            elif event.key == KEYS["LEFT"]:
                self.x -= 1
            elif event.key == KEYS["DOWN"]:
                self.y += 1
            elif event.key == KEYS["UP"]:
                self.y -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event.pos
            
game = GameController(20,20,35)
game.loadImages()
game.setBackgroundImage('borderTile.png')

#create an instance of your modified monster
character = myMonster(1, 1, 'circle.png')
dog = myMonster(1, 3, 'dog.png')

game.addGameObject(character)
game.addGameObject(dog)
game.drawMap()

game.run()
