from panda3d.core import Vec3, Point3
from direct.task import Task
from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from direct.showbase.DirectObject import DirectObject

class Inventory(DirectObject):
    def __init__(self):
        self.itemFrame = DirectScrolledFrame(
            text = "Inventory",
            text_scale = 0.25,
            text_pos = (0, 0.75, 0),
            text_bg = (1,1,1,1),
            # make the frame occupy the whole window
            frameSize = (-1.2, 1.2, -0.8, 0.8),
            # make the canvas as big as the frame
            canvasSize = (-1.2, 1.2, -0.8, 0.8),
            # set the frames color to white
            frameColor = (1, 1, 1, 1))
        self.itemList = []

    def show(self):
        self.itemFrame.show()

    def hide(self):
        self.itemFrame.hide()

    def __makeItem(self, item):
        obj = DirectLabel(
            text = str(item.giveLoot()) + "x " + item.giveType(),
            text_scale = 0.5,
            text_pos = (0, -1, 0),
            image = ("item.png", "item_hover.png", "item.png"), #normal, hover, disabled
            scale = 0.16,
            numStates = 2,
            state = DGG.NORMAL,
            relief = DGG.GROOVE)
        obj.setTransparency(True)
        obj["activeState"] = 0
        obj.reparentTo(self.itemFrame.getCanvas())
        obj.bind(DGG.B1PRESS, self.dragStart, [obj])
        obj.bind(DGG.B1RELEASE, self.dragStop)
        obj.bind(DGG.ENTER, self.inObject, [obj])
        obj.bind(DGG.EXIT, self.outObject, [obj])
        return obj

    def updateList(self, items):
        for item in self.itemList:
            item.destroy()
        i = 1
        j = 0
        pad = 0.2
        numItemsPerRow = 5
        itemWidth = 0.32
        itemHeight = 0.32
        left = -(itemWidth * (numItemsPerRow/2.0)) - 0.16
        xStep = itemWidth + 0.13
        yStep = -(itemHeight + 0.13)
        top = 0.8 - (0.16 + pad)
        for item in items:
            self.itemList.append(self.__makeItem(item))
            x = left + i * xStep
            y = top + j * yStep
            self.itemList[-1].setPos(x, 0.0, y)
            if i == numItemsPerRow:
                i = 0
                j += 1
            i += 1
        if i == 1: j-=1
        height = ((j) * -yStep) - 0.16
        print "HEIGT:", height
        # resize the canvas. This will make the scrollbars dis-/appear,
        # dependent on if the canvas is bigger than the frame size.
        self.itemFrame["canvasSize"] = (
            -0.8,
            0.8,
            -height,
            0.8)
        print self.itemFrame["canvasSize"]
        print self.itemFrame["frameSize"]

    def inObject(self, element, event):
        # Can be used to highlight objects
        element["activeState"] = 1
        element.setActiveState()
        #print "over object"

    def outObject(self, element, event):
        # Can be used to unhighlight objects
        #element["state"] = 0
        element["activeState"] = 0
        element.setActiveState()

    def dragStart(self, element, event):
        print "start drag"
        taskMgr.remove('dragDropTask')
        vWidget2render2d = element.getPos(render2d)
        vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
        editVec = Vec3(vWidget2render2d - vMouse2render2d)
        t = taskMgr.add(self.dragTask, 'dragDropTask')
        t.element = element
        t.editVec = editVec
        t.elementStartPos = element.getPos()

    def dragTask(self, state):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + state.editVec
            state.element.setPos(render2d, newPos)
        return Task.cont

    def dragStop(self, event):
        print "stop drag with:", event
        isInArea = False

        t = taskMgr.getTasksNamed('dragDropTask')[0]
        #for dropArea in self.dropAreas:
        #    if self.isInBounds(event.getMouse(), dropArea["frameSize"], dropArea.getPos(render)):
        #        print "inside Area:", dropArea["text"], dropArea.getPos(render)
        #        isInArea = True
        #        t.element.setPos(dropArea.getPos(render))
        #        t.element.setX(t.element.getX() * self.ratio)
        #        #t.element.setX(t.element.getX() - t.element.getWidth() / 2.0)
        #        break

        if not isInArea:
            t.element.setPos(t.elementStartPos)
        taskMgr.remove('dragDropTask')

    def isInBounds(self, location, bounds, posShift=None):
        x = 0 if posShift is None else posShift.getX()
        y = 0 if posShift is None else posShift.getZ()

        left = x + bounds[0]
        right = x + bounds[1]
        bottom = y + bounds[2]
        top = y + bounds[3]

        # are we outside of the bounding box from the left
        if location[0] < left: return False
        # are we outside of the bounding box from the right
        if location[0] > right: return False
        # are we outside of the bounding box from the bottom
        if location[1] < bottom: return False
        # are we outside of the bounding box from the top
        if location[1] > top: return False
        # the location is inside the bbox
        return True
