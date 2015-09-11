#!/usr/bin/python
#----------------------------------------------------------------------#

## IMPORTS ##
import sys

### PANDA Imports ###
from direct.showbase.ShowBase import ShowBase
from terrain import Terrain
from player import Player

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
        t = Terrain("map.png")

        p = Player()
        p.run()


game = Main()
game.run()
