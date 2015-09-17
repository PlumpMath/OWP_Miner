import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, GeomNode, CollisionTraverser
from panda3d.core import NodePath, PandaNode, CollisionNode, CollisionRay, CollisionHandlerQueue
from direct.showbase.DirectObject import DirectObject
from inventoryGui import Inventory

class Player(DirectObject):
    def __init__(self, _main):
        self.main = _main

        # Stats
        self.moveSpeed = 8
        self.inventory = []
        self.maxCarryWeight = 20.0 #kg ?
        self.currentInventoryWeight = 0.0

        # Inventory GUI
        self.inventoryGui = Inventory()
        self.inventoryGui.hide()
        self.inventoryActive = False

        # enable movements through the level
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
        self.player = NodePath("Player")#loader.loadModel("smiley")
        self.player.setPos(149.032, 329.324, 11.3384)
        self.player.setH(180)
        self.player.reparentTo(render)

        self.accept("w", self.setKey, ["forward",1])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("a", self.setKey, ["left",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("s", self.setKey, ["backward",1])
        self.accept("s-up", self.setKey, ["backward",0])
        self.accept("d", self.setKey, ["right",1])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("mouse1", self.handleLeftMouse)
        self.accept("i", self.toggleInventory)


        # screen sizes
        self.winXhalf = base.win.getXSize() / 2
        self.winYhalf = base.win.getYSize() / 2

        self.mouseSpeedX = 0.1
        self.mouseSpeedY = 0.1

        camera.setH(180)
        camera.reparentTo(self.player)
        camera.setZ(self.player, 2)
        base.camLens.setFov(75)
        base.camLens.setNear(0.8)

        # Mouse controls
        self.mouseNode = CollisionNode('mouseRay')
        self.mouseNodeNP = camera.attachNewNode(self.mouseNode)
        self.mouseNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.mouseRay = CollisionRay()
        self.mouseNode.addSolid(self.mouseRay)
        self.mouseRayHandler = CollisionHandlerQueue()

        # Collision Traverser
        self.traverser = CollisionTraverser("Player Traverser")
        base.cTrav = self.traverser
        self.traverser.addCollider(self.mouseNodeNP, self.mouseRayHandler)

    def run(self):
        taskMgr.add(self.move, "moveTask", priority=-4)

    def pause(self):
        taskMgr.remove("moveTask")

    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        if not base.mouseWatcherNode.hasMouse(): return task.cont

        pointer = base.win.getPointer(0)
        mouseX = pointer.getX()
        mouseY = pointer.getY()

        if base.win.movePointer(0, self.winXhalf, self.winYhalf):
            # calculate the looking up/down of the camera.
            # NOTE: for first person shooter, the camera here can be replaced
            # with a controlable joint of the player model
            p = camera.getP() - (mouseY - self.winYhalf) * self.mouseSpeedY
            if p <-80:
                p = -80
            elif p > 90:
                p = 90
            camera.setP(p)

            # rotate the player's heading according to the mouse x-axis movement
            h = self.player.getH() - (mouseX - self.winXhalf) * self.mouseSpeedX
            if h <-360:
                h = 360
            elif h > 360:
                h = -360
            self.player.setH(h)

        # basic movement of the player
        if self.keyMap["left"] != 0:
            self.player.setX(self.player, self.moveSpeed * globalClock.getDt())
        if self.keyMap["right"] != 0:
            self.player.setX(self.player, -self.moveSpeed * globalClock.getDt())
        if self.keyMap["forward"] != 0:
            self.player.setY(self.player, -self.moveSpeed * globalClock.getDt())
        if self.keyMap["backward"] != 0:
            self.player.setY(self.player, self.moveSpeed * globalClock.getDt())


        # keep the player on the ground
        elevation = self.main.t.terrain.getElevation(self.player.getX(), self.player.getY())
        self.player.setZ(elevation*self.main.t.zScale)

        return task.cont

    def toggleInventory(self):
        if self.inventoryActive:
            self.inventoryGui.hide()
            self.inventoryActive = False
            self.run()
        else:
            self.inventoryGui.show()
            self.inventoryActive = True
            self.pause()

    def handleLeftMouse(self):
        # Do the mining
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.mouseRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

            self.traverser.traverse(render)
            # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
            if self.mouseRayHandler.getNumEntries() > 0:
            # This is so we get the closest object.
                self.mouseRayHandler.sortEntries()
                pickedObj = self.mouseRayHandler.getEntry(0).getIntoNodePath()

                # Range check
                if (self.player.getPos() - pickedObj.getPos(render)).length() <= 3.0:
                    self.mine(pickedObj)
                else:
                    print "You are to far, move closer!"


    def mine(self, _nodeNP):
        self.nodeNP = _nodeNP

        # get the object class
        for node in self.main.nodeGen.currentNodes:
            # if mining node
            if self.main.nodeGen.currentNodes[node].model and self.main.nodeGen.currentNodes[node].model.getPos() == self.nodeNP.getPos(render):
                self.main.nodeGen.currentNodes[node].removeModel()
                self.inventory.append(self.main.nodeGen.currentNodes[node])
                self.currentInventoryWeight += self.main.nodeGen.currentNodes[node].weight
                self.inventoryGui.updateList(self.inventory)
                print "You received:", self.main.nodeGen.currentNodes[node].giveLoot(), self.main.nodeGen.currentNodes[node].giveType(), "Ores"
                print "Inventory:", self.inventory
                print "Current Weight:", self.currentInventoryWeight
                break

        print self.player.getPos()
