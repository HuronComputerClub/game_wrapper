#Example of the use of the game structure file

from gameFile import *

class myMonster(Monster):
    def onTurn(self, event = None):
        if event.key == KEYS["RIGHT"]:
            self.x += 1
        elif event.key == KEYS["LEFT"]:
            self.x -= 1
        elif event.key == KEYS["DOWN"]:
            self.y += 1
        elif event.key == KEYS["UP"]:
            self.y -= 1
            
game = GameController(15,15,20)
game.loadImages()
game.setBackgroundImage('borderTile.png')

#create an instance of your modified monster
character = myMonster(1, 1, 'circle.png')
dog = myMonster(1, 3, 'dog.png')

game.addGameObject(character)
game.addGameObject(dog)
game.drawMap()

game.run()
