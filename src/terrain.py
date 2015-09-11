#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import GeoMipTerrain, DirectionalLight, VBase4


########################################################################

class Terrain():

    def __init__(self, _heightField):

    	texture = loader.loadTexture("ground.png")
        
        self.terrain = GeoMipTerrain("BasicTerrain")
        self.terrain.setHeightfield(_heightField)
        self.terrain.getRoot().setSz(25)
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