#Example of the use of the game structure file

import gameFile#or from gameFile import *

game=gameFile.gameController()
game.loadImages()
game.setBackgroundImage('caveTile.png')
neatMonster=gameFile.monster(12, 10, 'dog.png')
game.addGameObject(neatMonster)
game.drawMap()

game.run()
