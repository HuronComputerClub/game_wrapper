#Example of the use of the game structure file

import gameFile#or from gameFile import *

class myMonster(gameFile.Monster):
    def onTurn(self):
        self.x -= 1

game = gameFile.gameController()
game.loadImages()
game.setBackgroundImage('borderTile.png')

#create an instance of your modified monster
neatMonster = myMonster(12, 10, 'circle.png')

game.addGameObject(neatMonster)
game.drawMap()

game.run()
