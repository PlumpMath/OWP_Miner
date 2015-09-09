#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
from terrain import Terrain


########################################################################

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Need First person character
        # - Basic pickaxe animation
        # Need Basic gui drag and drop
        # Need mining nodes
        t = Terrain("map.png")
        





game = Main()
game.run()
