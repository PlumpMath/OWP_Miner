#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import GeoMipTerrain, DirectionalLight, VBase4, CullBinAttrib, Fog, BitMask32


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

        self.skydome = loader.loadModel("Skydome")
        self.skydome.setDepthTest(False)
        self.skydome.setAttrib(CullBinAttrib.make("skydomeBin", 1000))
        self.skydome.reparentTo(camera)
        self.skydome.setScale(2)
        self.skydome.setPos(0, 0, -0.3)
        self.skydome.setCollideMask(BitMask32.allOff())
        taskMgr.add(self.skydomeTask, "paperplanet_skydome")

        # Add some fancy fog
        self.fog = Fog("Fog Name")
        self.fog.setColor(0.4,0.2,0.3)
        self.fog.setExpDensity(0.01)
        render.setFog(self.fog)

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

    def skydomeTask(self, task):
        self.skydome.setHpr(render, 0,0,0)
        return task.cont
