#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
from terrain import Terrain
from nodeGenerator import NodeGenerator


########################################################################

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Need First person character
        # - Basic pickaxe animation
        # Need Basic gui drag and drop
        # Need mining nodes
        self.t = Terrain("map.png")
        self.nodeGen = NodeGenerator(self, 100)

        #print render.ls()
        





game = Main()
game.run()
