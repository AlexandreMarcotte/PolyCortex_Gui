import pyqtgraph as pg
from PyQt5.QtWidgets import QScrollArea
from pyqtgraph.dockarea import DockArea, Dock
# --My Packages--
from V2.utils.btn import Btn
from V2.utils.rotated_button import RotatedButton


class InnerDock(Dock):
    def __init__(self, name='', size=(1, 1), external_layout=None,
                 b_checked=True, b_pos=None, toggle_btn=True, b_orientation=None,
                 set_scroll=False, add_dock_area=False, margin=(0, 0, 0, 0),
                 hide_title=True):

        super().__init__(
            name, size=size, hideTitle=hide_title, autoOrientation=False)

        self.b_pos = b_pos

        self.inner_layout = pg.LayoutWidget()

        self._create_toggle_button(
            toggle_btn, external_layout, name, b_orientation, b_checked)
        self._add_scroll_area(set_scroll)
        self._add_dock_area(add_dock_area, margin)
        if not b_checked:
            self.hide()

    def _add_scroll_area(self, set_scroll):
        if set_scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.addWidget(scroll)
            scroll.setWidget(self.inner_layout)
        else:
            self.addWidget(self.inner_layout)

    def _add_dock_area(self, add_dock_area, margin):
        if add_dock_area:
            self.dock_area = DockArea()
            self.dock_area.layout.setContentsMargins(*margin)
            self.inner_layout.addWidget(self.dock_area, 1, 0, 1, 6)

    def _create_toggle_button(
            self, toggle_btn, external_layout, name, b_orientation, b_checked):
        if toggle_btn:
            if b_orientation is not None:
                button = RotatedButton(
                    name, orientation=b_orientation)
                button.setMaximumWidth(20)
                button.setCheckable(True)
            else:
                button = Btn(name, toggle=True, max_height=18, font_size=10)
            if self.b_pos:
                external_layout.addWidget(button, *self.b_pos)
            else:
                external_layout.addWidget(button)
            button.clicked.connect(self._open)
            button.setChecked(b_checked)

    def _open(self, checked):
        if checked:
            self.show()
        else:
            self.hide()
