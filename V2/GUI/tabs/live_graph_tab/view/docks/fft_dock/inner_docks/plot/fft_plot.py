# -- General Packages --
from PyQt5.QtCore import pyqtSlot
from collections import defaultdict
# -- My Packages --
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.filter_region import FilterRegion
from V2.utils.colors import Color
from V2.general_settings import GeneralSettings


class FftPlot(ScrollPlotWidget):
    def __init__(self, curve_color=('w')):
        super().__init__(curve_color=curve_color)

        # self._add_filter_regions()
        self._ch_to_show = list(range(GeneralSettings.N_CH))
        self.filters = defaultdict(list)

    def _init_plot_appearance(self):
        # self.setYRange(0, 2000000) # auto
        self.setXRange(0, 125)
        self.plotItem.setLabel(axis='left', text='Amplitude')
        self.plotItem.setLabel(axis='bottom', text='Frequency')

    def connect_signals(self, signals, fft_stage=None):
        super().connect_signals(signals)
        self.fft_stage = fft_stage

    def _update(self):
        for ch in self._ch_to_show:
            self.curves[ch].setData(self.fft_stage.freq_range, self.signals[ch])

    # def _add_filter_regions(self):
    def create_filter_from_filter_stage(self, filter_stage):
        """Call from fft plot connector"""
        # Create filter from pipeline values
        min_boundary, max_boundary = filter_stage.cut_freq
        filter = FilterRegion(
                min_boundary=min_boundary, max_boundary=max_boundary,
                name=filter_stage.type)
        self.filters[filter_stage.type].append(filter)
        # Add filter to plot
        self.addItem(filter)
        return filter

    def change_curves_color(self, ch=0, color_btn=None):
        """pyqtSlot"""
        self.curves[ch].setPen(color_btn.color())

    def update_ch_to_show(self, ch):
        """pyqtSlot: Connect with ch on btn"""
        if ch == 'all':
            # Create a list with all the channels values
            self._ch_to_show = list(range(GeneralSettings.N_CH))
        else:
            # Get the int value in the string: Ch X
            self._ch_to_show = [int(ch[3:]) - 1]
        self._clear_curves()

    def _clear_curves(self):
        for c in self.curves:
            c.clear()
