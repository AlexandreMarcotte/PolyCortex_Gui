import pyqtgraph as pg
from PyQt5.QtWidgets import QScrollArea
from pyqtgraph.dockarea import DockArea, Dock
# --My Packages--
from V2.utils.btn import Btn
from V2.utils.rotated_button import RotatedButton


class InnerDock:
    def __init__(self, name='', size=(1, 1), main_layout=None, b_checked=True,
                 toggle_btn=True, b_orientation=None, background_color=None,
                 set_scroll=False, add_dock_area=False, margin=(1, 1, 1, 1),
                 hide_title=True):

        self._create_toggle_button(
            toggle_btn, main_layout, name, b_orientation, b_checked)
        self.layout = pg.LayoutWidget()
        self.dock = Dock(
            name, size=size, hideTitle=hide_title, autoOrientation=False)
        self._add_scroll_area(set_scroll)
        self._add_dock_area(add_dock_area, margin)
        self._set_plot_background_color(background_color)

    def _set_plot_background_color(self, background_color):
        if background_color is not None:
            pg.setConfigOption('background', background_color)

    def _add_scroll_area(self, set_scroll):
        if set_scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.dock.addWidget(scroll)
            scroll.setWidget(self.layout)
        else:
            self.dock.addWidget(self.layout)

    def _add_dock_area(self, add_dock_area, margin):
        if add_dock_area:
            self.dock_area = DockArea()
            self.dock_area.layout.setContentsMargins(*margin)
            self.layout.addWidget(self.dock_area, 1, 0, 1, 6)

    def _create_toggle_button(
            self, toggle_btn, main_layout, name, b_orientation, b_checked):
        if toggle_btn:
            if b_orientation is not None:
                button = RotatedButton(
                        name, orientation=b_orientation)
                button.setMaximumWidth(20)
                button.setCheckable(True)
            else:
                button = Btn( name, toggle=True, max_height=18, font_size=10)

            main_layout.addWidget(button)
            button.clicked.connect(self._open)
            button.setChecked(b_checked)

    def _open(self, checked):
        if checked:
            self.dock.show()
        else:
            self.dock.hide()
