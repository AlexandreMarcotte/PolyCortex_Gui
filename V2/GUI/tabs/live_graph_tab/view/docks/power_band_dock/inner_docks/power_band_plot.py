# --General Packages--
from pyqtgraph.dockarea import Dock
from PyQt5 import QtCore
import pyqtgraph as pg
# --My Packages--
from V2.pipeline.pipeline_stages.fft_stage.fft_stage import FftStage
from V2.utils.waves import waves


class PowerBandPlot(Dock):
    def __init__(self, ):
        super().__init__(name='', hideTitle=True)
        self.ch = 0

        self.plot = self.init_plot()
        self.addWidget(self.plot)
        # self.brushes, self.x, self.width = self.init_bar_graph_caract()
        self.N_ELE = len(waves)

        self._connect_timer()

    def _connect_timer(self):
        self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self._update)

    def start_timer(self):
        self.timer.start(20)

    def connect_signal(self, fft_stage: FftStage):
        self.fft_stage = fft_stage
        self.fft_over_time = self.fft_stage.fft_over_time

    def init_plot(self):
        plot = pg.PlotWidget()
        waves_names = [wave_name for wave_name in waves]
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.setLabel(axis='bottom', text=waves_names)
        return plot

    """
    def init_bar_graph_caract(self):
        brushes = [pg.mkBrush(i) for i in range(len(waves))]
        x = [w.get_half_pos() for w in waves.values()]
        width = [w.get_delta_range() for w in waves.values()]

        return brushes, x, width

    def _update(self):
        self.plot.clear()
        bg = pg.BarGraphItem(
            height=self.fft_stage.freq_per_band_all_ch[self.ch],              # put the function directly here
            # height=partial(self.gv.freq_calculator.get_avg_freq_per_band, 0),
            x=self.x, width=self.width, brushes=self.brushes)
        self.plot.addItem(bg)
    """
