from pyqtgraph.dockarea import *
import pyqtgraph as pg
from functools import partial
# --My packages--
from V2.utils.btn import Btn
from V2.utils.lable_btn import LabelBtn
from V2.utils.colors import *
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class EegPlotDock(PlotDock):
    def __init__(self, ch):
        self._ch = ch
        curve_color = pen_colors[ch]
        super().__init__(curve_color=curve_color)

        self._add_all_btn()

    def _add_all_btn(self):
        # Just for visualisation test at the moment
        self.toggle_btn = self._add_toggle_on_off_btn()
        self._add_action_btn()

    def _add_toggle_on_off_btn(self):
        toggle_btn = Btn(
            name=str(self._ch+1), max_width=23, max_height=23,
            color=button_colors[self._ch], txt_color=black,
            toggle=True, tip=f'Start/Stop the ch{self._ch+1} signal')

        self.addWidget(toggle_btn, 0, 0, 1, 1)
        return toggle_btn

    def _add_action_btn(self):
        # Average btn
        self.avg_value_btn = LabelBtn(
            name='A', tip='Show average value of queue', conn_func='avg')
        # Maximum btn
        self.max_value_btn = LabelBtn(
            name='M', tip='Show maximum value of queue', conn_func='max')
        #  btn
        self.fft_size_btn = LabelBtn(
            name='F', tip='''Show the size of the fft window on 
                which the fft is calculated for all ch''')

        for no, btn in enumerate(
                [self.avg_value_btn, self.max_value_btn, self.fft_size_btn]):
            self.addWidget(btn, no, 10, 1, 1)
            self.addWidget(btn.label, no, 9, 1, 1)

        self.create_color_button()

    def create_color_button(self):
        """Create color button to change the color of the line"""
        color_btn = pg.ColorButton()
        color_btn.setMaximumWidth(23)
        color_btn.setMaximumHeight(23)
        color_btn.setToolTip('Click to change the color of the line')
        color_btn.sigColorChanged.connect(partial(self.change_line_color))
        self.addWidget(color_btn, 3, 10)

    def change_line_color(self):
        print('change color')
        # color = color_btn.color()
        # self.eeg_graphes[self.ch].curve.setPen(color)
        # self.gv.curve_freq[self.ch].setPen(color)
        # self.btns[self.ch].set_color(color)
