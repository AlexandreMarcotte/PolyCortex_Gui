from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.filter_region import FilterRegion
from V2.utils.colors import Color


class FftPlot(ScrollPlotWidget):
    def __init__(self, curve_color=('w')):
        super().__init__(curve_color=curve_color)

        self._add_filter_regions()

    def _init_plot_appearance(self):
        # self.setYRange(0, 2000000) # auto
        self.setXRange(0, 125)
        self.plotItem.setLabel(axis='left', text='Amplitude')
        self.plotItem.setLabel(axis='bottom', text='Frequency')

    def _add_filter_regions(self):
        # Bandpass
        # self.band_pass = FilterRegion(min_boundary=2, max_boundary=80)
        # self.addItem(self.band_pass)
        # Bandcut
        self.band_cut = FilterRegion(
            min_boundary=56, max_boundary=64, color=Color.red)
        self.addItem(self.band_cut)

    def connect_signals(self, signals, fft_stage=None):
        super().connect_signals(signals)
        self.fft_stage = fft_stage

    def _update(self):
        for i, signal in enumerate(self.signals):
            self.curves[i].setData(self.fft_stage.freq_range, signal)

    def change_curves_color(self, ch=0, color_btn=None):
        self.curves[ch].setPen(color_btn.color())

