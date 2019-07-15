from app.colors import *
import pyqtgraph as pg
from abc import abstractclassmethod
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPen
# -- My Packages --
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

    @abstractclassmethod
    def _create_all_combobox(self):
        """Overload this method to create the combobox to act on the dock graph"""

    def start_aliasing(self, txt):  # Need to do it before creating the graph
        # (don't work here but work when called in the main at the start)
        # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
        if txt == 'on':
            pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
        elif txt == 'off':
            pg.setConfigOptions(antialias=False)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        qp.setPen(QColor(200, 200, 200))
        qp.setBrush(QColor(210, 215, 215))
        qp.drawRect(0, 0, 3000, 36)
