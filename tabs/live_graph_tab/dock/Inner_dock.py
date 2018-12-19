# --General Packages--
import pyqtgraph as pg
from PyQt5 import QtCore
from pyqtgraph.dockarea import *
# --My Packages--
from app.activation_b import btn


class InnerDock:
    def __init__(self, main_layout, name, b_pos=(0, 0), b_checked=True,
                 toggle_button=False, size=None):
        self.b_pos = b_pos
        self.b_checked = b_checked
        self.toggle_button = toggle_button
        self.size = size

        self.dock, self.layout = self.create_dock(main_layout, name)

    def create_dock(self, main_layout, name):
        if self.size is not None:
            dock = Dock(name, size=self.size)
        else:
            dock = Dock(name)
        dock.hideTitleBar()
        if self.toggle_button:
            self.create_button(main_layout, name)
        layout = pg.LayoutWidget()
        dock.addWidget(layout)
        return dock, layout

    def create_button(self, main_layout, name):
        button = btn(
            name, main_layout, self.b_pos, func_conn=self.open, toggle=True,
            max_height=18, font_size=10)
        button.b.setChecked(self.b_checked)

    @QtCore.pyqtSlot(bool)
    def open(self, checked):
        if checked:
            self.dock.show()
        else:
            self.dock.hide()
