import pyqtgraph as pg
from PyQt5 import QtGui, QtCore


class ColorBtn(pg.ColorButton):
    def __init__(self, parent=None, color=(255,255,255)):
        super().__init__(parent=None, color=color)
        self.setMaximumWidth(23)
        self.setMaximumHeight(23)
        self.setToolTip('Click to change the color of the line')

    def paintEvent(self, ev):
        QtGui.QPushButton.paintEvent(self, ev)
        p = QtGui.QPainter(self)
        rect = self.rect().adjusted(0, 0, -1, -1)
        ## draw white base, then texture for indicating transparency, then actual color
        p.setBrush(pg.functions.mkBrush('w'))
        p.drawRect(rect)
        p.setBrush(QtGui.QBrush(QtCore.Qt.DiagCrossPattern))
        p.drawRect(rect)
        p.setBrush(pg.functions.mkBrush(self._color))
        p.drawRect(rect)
        p.end()
