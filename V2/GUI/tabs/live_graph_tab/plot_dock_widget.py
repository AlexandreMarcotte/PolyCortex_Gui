from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from pyqtgraph.dockarea.Dock import DockLabel
from V2.utils.update_style_patch import update_style_patched


class PlotDockWidget(Dock):
    def __init__(self, name, plot):
        DockLabel.updateStyle = update_style_patched
        super().__init__(name)
        self.addWidget(plot, 0, 1, 3, 1)
        self.addWidget(QPushButton('A'), 0, 0, 1, 1)
        for i in range(3):
            self.addWidget(QPushButton(str(i)), i, 2, 1, 1)
