# -- General Packages --
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from pyqtgraph.dockarea import *

# -- My Packages --
from app.activation_b import btn
from app.pyqt_frequently_used import *
from tabs.live_graph_tab.dock.inner_dock import InnerDock


class Dock:
    def __init__(self, gv, dock_type, secondary_layout):
        self.gv = gv
        self.type = dock_type
        self.secondary_layout = secondary_layout

        self.timer = QtCore.QTimer()

        self.init_dock_area()
        self.settings_d = self.init_settings_dock()
        self.plot_d = self.init_plot_dock()

    def init_dock_area(self):
        self.dock_area = DockArea()
        self.secondary_layout.addWidget(self.dock_area, 1, 0, 1, 8)

    def init_settings_dock(self):
        settings_d = InnerDock(
            self.secondary_layout, 'Settings', toggle_button=True,
            size=(1, 1))
        self.dock_area.addDock(settings_d.dock)
        return settings_d

    def init_plot_dock(self):
        plot_d = InnerDock(self.secondary_layout, 'Plot')
        self.dock_area.addDock(plot_d.dock)
        return plot_d

    def init_choose_ch_combobox(self):
        create_param_combobox(
            self.settings_d.layout, 'Channel', (0, 1),
            [str(ch+1) for ch in range(self.gv.N_CH)],
            self.print_ch, editable=False)

    def print_ch(self, ch):
        self.ch = int(ch) - 1

    def init_on_off_button(self):
        btn('Start', self.settings_d.layout, (0, 0), func_conn=self.start,
            color=dark_blue_tab, toggle=True, txt_color=white, max_width=100,
            min_width=100)

    @pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(200)
        else:
            self.timer.stop()
            self.gv.freq_calculator.timer.stop()
            self.gv.freq_calculator.activated = False

        if self.type == 'fft':
            if checked:
                self.gv.freq_calculator.timer.start(100)
                self.gv.freq_calculator.activated = True
