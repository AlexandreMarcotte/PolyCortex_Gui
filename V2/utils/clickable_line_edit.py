from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal


class ClickableLineEdit(QLineEdit):
    def __init__(self, i, name):
        super().__init__()
        self.i = i
        self.name = name

        self.planes = ['x', 'y', 'z']
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        pass
        # self.clicked.emit()
        # if self.name == 'position':
        #     self.gv.plane_to_move = self.planes[self.i]
        # if self.name == 'angle':
        #     self.gv.rotation_axis = self.planes[self.i]
        #     print('angle', self.i)
        # QLineEdit.mousePressEvent(self, event)
