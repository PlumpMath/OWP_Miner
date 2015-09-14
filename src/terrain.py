#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import GeoMipTerrain, DirectionalLight, VBase4


########################################################################

class Terrain():

    def __init__(self, _heightField):

    	texture = loader.loadTexture("ground_tex.png")
        self.zScale = 45
        
        self.terrain = GeoMipTerrain("BasicTerrain")
        self.terrain.setHeightfield(_heightField)
        self.terrain.getRoot().setSz(self.zScale)
        self.terrain.getRoot().setTexture(texture)
        self.terrain.getRoot().reparentTo(render)
        self.terrain.generate()

        self.terrainSize = (self.terrain.heightfield().getReadXSize(), self.terrain.heightfield().getReadYSize())
        print "Terrain Size:", self.terrainSize

        # Some Test light
        dlight = DirectionalLight("dlight")
        dlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)


        # Add basic blacksmith hut
        tmp = loader.loadModel("blacksmith_hut")
        tmp.reparentTo(render)
        tmp.setPos(164.054, 340.92, 11.3384)
