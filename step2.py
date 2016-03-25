#Step 2
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 2, 'cat.png')
game.addGameObject(player)

for x in range(10):
    #put walls down at (x,y)
    pass


game.run()
