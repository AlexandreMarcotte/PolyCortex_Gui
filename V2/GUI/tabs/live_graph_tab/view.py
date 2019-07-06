from pyqtgraph.dockarea import *
import pyqtgraph as pg
from PyQt5.QtWidgets import *
# --My packages--
from .docks.eeg_dock.eeg_dock import EegDock


class View(QWidget):
    def __init__(self, model):
        super().__init__()

        self._model = model

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self.init_docks()

    def init_docks(self):
        self.eeg_dock = self.init_eeg_dock()

    def init_eeg_dock(self):
        eeg_dock = EegDock(self)
        self.area.addDock(eeg_dock)
        return eeg_dock


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

