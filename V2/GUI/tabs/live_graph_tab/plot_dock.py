from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from pyqtgraph.dockarea.Dock import DockLabel
from V2.utils.update_style_patch import update_style_patched


class PlotDock(Dock):
    def __init__(self, name, plot):
        # self.name = name
        self.scroll_plot = plot

        DockLabel.updateStyle = update_style_patched
        super().__init__(name)

        self.add_plot(plot)
        self.add_controller_btn()

    def add_plot(self, plot):
        self.addWidget(plot, 0, 1, 3, 1)

    def add_controller_btn(self):
        # Just for visualisation test at the moment
        self.addWidget(QPushButton('A'), 0, 0, 1, 1)
        for i in range(3):
            self.addWidget(QPushButton(str(i)), i, 2, 1, 1)
