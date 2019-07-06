from PyQt5 import QtGui
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import *


class MyDock(Dock):
    def __init__(self, name, size=(1, 1), hide_title=False, set_scroll=True,
                 margin=(10, 6, 6, 6)):
        super().__init__(name, size=size, hideTitle=hide_title, area=DockArea())

        layout = pg.LayoutWidget()

        self.set_scrolling_area(set_scroll, layout)

        self.dock_area = DockArea()
        self.dock_area.layout.setContentsMargins(*margin)
        self.layout.addWidget(self.dock_area, 1, 0, 1, 1)

    def set_scrolling_area(self, set_scroll, layout):
        if set_scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.addWidget(scroll)
            self.layout = layout
            scroll.setWidget(self.layout)
        else:
            self.layout = layout
            self.addWidget(self.layout)


