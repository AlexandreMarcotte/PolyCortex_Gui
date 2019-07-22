from app.colors import *
import pyqtgraph as pg
from abc import abstractclassmethod
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPen
# -- My Packages --
from V2.utils.parameter_combobox import ParameterCombobox
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.utils.btn import Btn


class SettingsDock(InnerDock):
    def __init__(self, main_layout):
        super().__init__(external_layout=main_layout, name='Settings',
                         fixed_height=73)
        self.external_layout = main_layout

    def _create_settings_dock(self):
        # Stop/Start button
        self._create_start_buttons()

    def _create_start_buttons(self):
        """Assign pushbutton for starting"""
        self.start_btn = Btn('Start', toggle=True)
        self.inner_layout.addWidget(self.start_btn, 0, 0)

    def create_choose_channel_cb(self):
        self.scale_freq_axis_cb = ParameterCombobox(
            self.inner_layout, 'Channel', (0, 1), [str(i+1) for i in range(8)],
            editable=False)

    @abstractclassmethod
    def _create_all_combobox(self):
        """Overload this method to create the combobox to act on the dock graph"""

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_grey_rectangle(qp)
        qp.end()

    def _draw_grey_rectangle(self, qp):
        w = self.size().width()
        h = self.size().height()
        qp.setPen(QColor(210, 215, 255))
        qp.setBrush(QColor(210, 215, 255))
        # Pale layout blue up
        qp.drawRect(0, 10, w, 26)
        qp.drawRoundedRect(
            0, 0, w, 15, 8, 8)
        # Cream layout down
        qp.setPen(QColor(249, 248, 245))
        qp.setBrush(QColor(249, 248, 245))
        qp.drawRect(0, 38, w, 26)
        qp.drawRoundedRect(
            0, h-10, w, 10, 8, 8)
