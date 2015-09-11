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

    def __init__(self, _main, _numOfNodes):
    	self.main = _main
    	self.numOfNodes = _numOfNodes
    	self.currentNodes = {}

    	self.placeNodes()

    def generateNode(self, _id):
    	self.currentNodes[_id] = Node()

    def placeNodes(self):
    	for i in xrange(self.numOfNodes):
    		x = random.random() * self.main.t.terrainSize[0]
    		y = random.random() * self.main.t.terrainSize[1]

    		if random.random() < self.main.t.terrain.getElevation(x, y):
    			elevation = self.main.t.terrain.getElevation(x, y)
    			self.generateNode(i)
    			self.currentNodes[i].model.setPos(x, y, elevation*25)

    def respawnQueue(self):
    	pass



class Node():

	def __init__(self):
		types = ['copper', 'iron', 'silver', 'gold']

		self.type = random.choice(types)
		self.lootAmount = random.randint(1, 8)
		self.respawnTime = random.randint(300, 3600) # 5mins - 60mins, Maybe a bit heavy but whatever
		self.position = (0, 0, 0)
		self.model = None
		self.collisionShape = None

		self.model = loader.loadModel("ball")
		self.model.reparentTo(render)
		self.model.setPos(self.position)
		self.model.setScale(0.5)

		print "Created:", self.type, "Node, Value:", self.lootAmount, "RespawnTime:", self.respawnTime

	def setCollisionShape(self):
		pass

	def setModel(self):
		pass

	def setPosition(self):
		pass
