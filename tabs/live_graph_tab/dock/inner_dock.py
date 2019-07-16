from PyQt5 import QtCore
from pyqtgraph.dockarea import *
from functools import partial
import pyqtgraph as pg
# --My Packages--
from app.activation_b import btn
from app.rotated_button import RotatedButton


class InnerDock:
    def __init__(self, main_layout, name, b_pos=(0, 0), b_checked=True,
                 toggle_button=False, size=(1, 1), b_orientation=None,
                 background_color=None):
        self.b_pos = b_pos
        self.b_checked = b_checked
        # self.toggle_button = toggle_button
        self.size = size
        self.b_orientation = b_orientation
        # self.background_color = background_color
        self.dock, self.layout = self.init_dock(
            main_layout, name, toggle_button)

    def init_dock(self, main_layout, name, toggle_button):
        if self.size is not None:
            dock = Dock(name, size=self.size)
        else:
            dock = Dock(name)
        dock.hideTitleBar()
        if toggle_button:
            self._create_toggle_button(main_layout, name)
        layout = pg.LayoutWidget()
        # if self.background_color is not None:
        #     pg.setConfigOption('background', self.background_color)
        dock.addWidget(layout)
        return dock, layout

    def _create_toggle_button(self, main_layout, name):
        if self.b_orientation is not None:
            button = RotatedButton(
                    name, orientation=self.b_orientation)
            button.clicked.connect(self.open)
            main_layout.addWidget(button, *self.b_pos)
        else:
            button = btn(
                    name, main_layout, self.b_pos, func_conn=self.open,
                    toggle=True, max_height=18, font_size=10)
            button.b.setChecked(self.b_checked)

    # @QtCore.pyqtSlot(bool)
    def open(self, checked):
        if checked:
            self.dock.show()
        else:
            self.dock.hide()
