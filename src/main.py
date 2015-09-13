#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from terrain import Terrain
from player import Player
from nodeGenerator import NodeGenerator

loadPrcFileData('', 'win-size 1024 600')

########################################################################

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # accept the esc button to close the application
        self.accept("escape", sys.exit)

        # disable pandas default mouse-camera controls so we can handle the cam
        # movements by ourself
        self.disableMouse()

        # Need First person character
        # - Basic pickaxe animation
        # Need Basic gui drag and drop
        # Need mining nodes
        self.t = Terrain("heightmap.png")
        self.nodeGen = NodeGenerator(self, 100)

        #print render.ls()

        self.p = Player(self)
        self.p.run()


game = Main()
game.run()
