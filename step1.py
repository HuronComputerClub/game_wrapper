#Step 1
import pygame

from gameFile import *
#Game already exists
#1 coin automatically on board
#score increments automatically


#create a player character
player = Player(1, 2, 'person.png')
game.addGameObject(player)
game.run()
