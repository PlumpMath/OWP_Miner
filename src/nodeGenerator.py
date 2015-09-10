#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys
import random

### PANDA Imports ###


########################################################################

## Common Ores ##
# Copper
# Iron
# Silver
# Gold
#################

class NodeGenerator():

    def __init__(self, _type):

    	self.types = ['copper', 'iron', 'silver', 'gold']

    def generateNode(self):
    	pass

    def respawnQueue(self):
    	pass



class Node():

	def __init__(self):

		self.type = random.choice(self.types)
		self.lootAmount = random.randint(1, 8)
		self.respawnTime = random.randint(300, 3600) # 5mins - 60mins, Maybe a bit heavy but whatever
		self.positon = (0, 0, 0)
		self.model = None
		self.collisionShape = None

	def setCollisionShape(self):
		pass

	def setModel(self):
		pass

	def setPosition(self):
		pass
