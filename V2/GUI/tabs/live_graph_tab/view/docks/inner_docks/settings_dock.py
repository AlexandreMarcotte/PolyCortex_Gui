from abc import abstractclassmethod
from PyQt5.QtGui import QColor
# -- My Packages --
from V2.utils.parameter_combobox import ParameterCombobox
from V2.GUI.tabs.inner_dock import InnerDock
from V2.utils.btn import Btn


class SettingsDock(InnerDock):
    def __init__(self, main_layout):
        super().__init__(external_layout=main_layout, name='Settings',
                         fixed_height=73)
        self.external_layout = main_layout

    def _create_settings_dock(self):
        """Stop/Start button"""
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

    def _draw_background(self, qp):
        w = self.size().width()
        h = self.size().height()
        self._draw_half_blue_background(qp, w)
        self._draw_half_cream_background(qp, w, h)

    def _draw_half_blue_background(self, qp, w):
        qp.setPen(QColor(210, 215, 255))
        qp.setBrush(QColor(210, 215, 255))
        qp.drawRect(0, 10, w, 26)
        qp.drawRoundedRect(
            0, 0, w, 15, 8, 8)

    def _draw_half_cream_background(self, qp, w, h):
        qp.setPen(QColor(249, 248, 245))
        qp.setBrush(QColor(249, 248, 245))
        qp.drawRect(0, 38, w, 26)
        qp.drawRoundedRect(0, h-10, w, 10, 8, 8)


