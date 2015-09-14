from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectLabel
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

    def __makeItem(self, item, x, y):
        obj = DirectLabel(
            text = "testText",
            text_scale = 0.5,
            image = "item.png",
            scale = 0.16,
            pos = (x, 0, y))
        obj.reparentTo(self.itemFrame.getCanvas())
        return obj

    def updateList(self, items):
        for item in self.itemList:
            item.destroy()
        i = 1
        j = 0
        left = -1.2 + 0.32
        top = 0.8 - 0.32
        for item in items:
            x = left + i * 0.32
            y = top + j * -0.32
            self.itemList.append(self.__makeItem(item, x, y))
            if i == 7:
                i = 0
                j += 1
            i += 1
        height = len(self.itemList)/10 * 0.16
        # resize the canvas. This will make the scrollbars dis-/appear,
        # dependent on if the canvas is bigger than the frame size.
        self.itemFrame["canvasSize"] = (
            -0.8,
            0.8,
            height,
            0.8)
