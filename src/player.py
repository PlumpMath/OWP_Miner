import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.core import NodePath, PandaNode, CollisionNode, CollisionRay, CollisionHandlerFloor
from direct.showbase.DirectObject import DirectObject

class Player(DirectObject):
    def __init__(self, _main):
        self.main = _main

        # Stats
        self.moveSpeed = 8

        # enable movements through the level
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
        self.player = NodePath("Player")#loader.loadModel("smiley")
        self.player.setPos(0, 0, 1)
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

    def run(self):
        taskMgr.add(self.move, "moveTask", priority=-4)

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
