# -- General Packages --
from PyQt5.QtCore import pyqtSlot
# -- My Packages --
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.filter_region import FilterRegion
from V2.utils.colors import Color
from V2.general_settings import GeneralSettings


class FftPlot(ScrollPlotWidget):
    def __init__(self, curve_color=('w')):
        super().__init__(curve_color=curve_color)

        self._add_filter_regions()
        self._ch_to_show = list(range(GeneralSettings.N_CH))

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

    def _add_filter_regions(self):
        # Bandpass
        # self.band_pass = FilterRegion(min_boundary=2, max_boundary=80)
        # self.addItem(self.band_pass)
        # Bandcut
        self.band_cut = FilterRegion(
            min_boundary=56, max_boundary=64, color=Color.red)
        self.addItem(self.band_cut)

    def change_curves_color(self, ch=0, color_btn=None):
        """pyqtSlot"""
        self.curves[ch].setPen(color_btn.color())

    def update_ch_to_show(self, ch):
        """pyqtSlot: Connect with ch on btn"""
        if ch == 'all':
            self._ch_to_show = list(range(GeneralSettings.N_CH))
        else:
            self._ch_to_show = [int(ch[3:]) - 1]
        self._clear_curves()

    def _clear_curves(self):
        for c in self.curves:
            c.clear()
