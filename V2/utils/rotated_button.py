from PyQt5 import QtCore
from PyQt5.QtWidgets import *
# --My Packages--
from V2.utils.btn import Btn


class RotatedButton(Btn):
    def __init__(self, text, orientation="west"):
        super().__init__(text, font_size=9)
        self.orientation = orientation
        self.setMaximumWidth(20)
        self.setCheckable(True)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        if self.orientation == 'west':
            painter.rotate(90)
            painter.translate(0, -1 * 20)
        elif self.orientation == 'east':
            painter.rotate(270)
            painter.translate(-1 * self.height(), 0)
        painter.drawControl(QStyle.CE_PushButton, self.getSyleOptions())
        # self.setStyleSheet(f'''font-size: {9}pt;''')

    def sizeHint(self):
        size = super(RotatedButton, self).sizeHint()
        size.transpose()
        return size

    def getSyleOptions(self):
        options = QStyleOptionButton()
        options.initFrom(self)
        size = QtCore.QSize(80, 18)
        options.rect.setSize(size)
        options.text = self.text()
        return options
