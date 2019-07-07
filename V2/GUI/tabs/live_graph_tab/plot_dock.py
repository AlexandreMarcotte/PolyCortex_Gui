from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from pyqtgraph.dockarea.Dock import DockLabel
from V2.utils.update_style_patch import update_style_patched
from V2.utils.activation_btn import ActivationBtn
from V2.utils.colors import *


class PlotDock(Dock):
    def __init__(self, ch, plot):
        self._ch = ch
        self.scroll_plot = plot

        DockLabel.updateStyle = update_style_patched
        super().__init__(str(ch), hideTitle=True)

        self._add_plot(plot)
        self._add_all_btn()

    def _add_plot(self, plot):
        self.addWidget(plot, 0, 1, 3, 1)

    def _add_all_btn(self):
        # Just for visualisation test at the moment
        self.activation_btn = self._add_activation_btn()
        self._add_action_btn()

    def _add_activation_btn(self):
        activation_btn = ActivationBtn(
                name=str(self._ch+1), max_width=19, max_height=19,
                color=button_colors[self._ch], toggle=True,
                tip=f'Start/Stop the ch{self._ch+1} signal')

        self.addWidget(activation_btn, 0, 0, 1, 1)
        return activation_btn

    def _add_action_btn(self):
        # self.btn = btn(
        #         name=str(ch + 1), layout=ch_layout, pos=(0, 0),
        #         func_conn=ch_number_action.stop_ch, color=button_colors[ch],
        #         toggle=True, max_width=19, max_height=19,
        #         tip=f'Start/Stop the ch{ch+1} signal')
        for i in range(3):
            self.addWidget(QPushButton(str(i)), i, 2, 1, 1)
