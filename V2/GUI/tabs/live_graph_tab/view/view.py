from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from .docks.eeg_dock.eeg_dock import EegDock
from .docks.fft_dock.fft_dock import FftDock


class View(QWidget):
    def __init__(self):
        super().__init__()

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self.init_docks()

    def init_docks(self):
        self.eeg_dock = self._init_eeg_dock()
        self.fft_dock = self._init_fft_dock()

    def _init_eeg_dock(self):
        eeg_dock = EegDock()
        self.area.addDock(eeg_dock.dock)
        return eeg_dock

    def _init_fft_dock(self):
        fft_dock = FftDock()
        self.area.addDock(fft_dock.dock, 'right', self.eeg_dock.dock)
        return fft_dock





        # fft_dock = EegDock()
        # self.area.addDock(fft_dock, 'right', self.eeg_dock)
        # return fft_dock

        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Filter Sig out & in',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.filter_stage.output,
        #                  self._model.pipeline.filter_stage.input])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Timestamp',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.signal_collector.timestamps])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='FFT',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Spectogram',
        #     plot=SpectogramPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))

