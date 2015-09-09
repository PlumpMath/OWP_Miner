#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import GeoMipTerrain


########################################################################

class Terrain():

    def __init__(self, _heightField):
        
        self.terrain = GeoMipTerrain("BasicTerrain")
        self.terrain.setHeightfield(_heightField)
        self.terrain.getRoot().reparentTo(render)
        self.terrain.generate()