#Example of the use of the game structure file

import gameFile#or from gameFile import *

game=gameFile.gameController()
game.loadImages()
game.setBackgroundImage('borderTile.png')
neatMonster=gameFile.monster(12, 10, 'circle.png')
game.addGameObject(neatMonster)
game.drawMap()

game.run()
