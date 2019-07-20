from functools import partial
from PyQt5.QtWidgets import *
# --My packages--
from V2.utils.btn import Btn
from V2.utils.lable_btn import LabelBtn
from V2.utils.colors import Color
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
from V2.utils.color_btn import ColorBtn
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.pins_settings.pins_settings import PinSettings
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class EegPlotDock(PlotDock):
    def __init__(self, ch):
        self._ch = ch
        self.curve_color = (Color.pen_colors[ch])
        super().__init__(ScrollPlotWidget(self.curve_color))
        self._add_all_btn()

    def _add_all_btn(self):
        # Just for visualisation test at the moment
        self.toggle_btn = self._add_toggle_on_off_btn()
        self._add_action_btn()

    def _add_toggle_on_off_btn(self):
        toggle_btn = Btn(
            name=str(self._ch+1), max_width=23, max_height=39,
            color=Color.button_colors[self._ch], txt_color=Color.black,
            toggle=True, tip=f'Start/Stop the ch{self._ch+1} signal')

        self.addWidget(toggle_btn, 0, 0)
        return toggle_btn

    def _add_action_btn(self):
        # Average btn
        self.avg_value_btn = LabelBtn(
            name='A', tip='Show average value of queue', conn_func='avg',
            plot=self.plot)
        # Maximum btn
        self.max_value_btn = LabelBtn(
            name='M', tip='Show maximum value of queue', conn_func='max',
            plot=self.plot)
        #  btn
        self.fft_size_btn = LabelBtn(
            name='F', tip='''Show the size of the fft window on 
                which the fft is calculated for all ch''')
        self.action_btns = [
            self.avg_value_btn, self.max_value_btn, self.fft_size_btn]
        for no, btn in enumerate(self.action_btns):
            self.addWidget(btn, no, 6)
            self.addWidget(btn.label, no, 5)

        self.create_color_button()

        self.add_pin_setting_cb()

    def add_pin_setting_cb(self):
        self.pins_settings = PinSettings()
        self.pins_settings.add_pin_settings_to_layout(self)
        self.pins_settings.hide_pins_settings()

    def create_color_button(self):
        """Create color button to change the color of the line"""
        color_btn = ColorBtn(color=self.curve_color)
        color_btn.sigColorChanged.connect(partial(self.change_line_color))
        self.addWidget(color_btn, 3, 6)

    def change_line_color(self):
        print('change color')
        # color = color_btn.color()
        # self.eeg_graphes[self.ch].curve.setPen(color)
        # self.gv.curve_freq[self.ch].setPen(color)
        # self.btns[self.ch].set_color(color)
