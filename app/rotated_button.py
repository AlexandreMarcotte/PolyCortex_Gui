from PyQt5 import QtCore
from PyQt5.QtWidgets import *

class RotatedButton(QPushButton):
    def __init__(self, text, parent, orientation="west"):
        super().__init__(text, parent)
        self.orientation = orientation

    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.rotate(90)
        painter.translate(0, -1*20)
        painter.drawControl(QStyle.CE_PushButton, self.getSyleOptions())

    def sizeHint(self):
        size = super(RotatedButton, self).sizeHint()
        size.transpose()
        return size

    def getSyleOptions(self):
        options = QStyleOptionButton()
        options.initFrom(self)
        size = QtCore.QSize(80, 20)
        options.rect.setSize(size)
        options.text = self.text()
        return options

