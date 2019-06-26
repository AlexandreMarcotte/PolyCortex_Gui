from pyqtgraph.dockarea import *
import pyqtgraph as pg
from PyQt5.QtWidgets import *
# --My packages--
from .plot_dock_widget import PlotDockWidget
from .plot_widgets.scroll_plot_widget import ScrollPlotWidget
from .plot_widgets.spectrogram_plot_widget import SpectogramPlotWidget
from .docks.inner_dock import InnerDock
from .docks.eeg_dock.my_dock import MyDock
from .docks.eeg_dock.inner_docks.settings_dock import SettingsDock
from tabs.live_graph_tab.dock.inner_dock import InnerDock


class View(QWidget):
    def __init__(self, model):
        super().__init__()

        self._model = model

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self.init_docks()

    def init_docks(self):

        eeg_dock = MyDock('EEG')
        self.area.addDock(eeg_dock)

        # settings_layout = layout = pg.LayoutWidget()
        # eeg_dock.layout.addWidget(settings_layout)
        settings_dock = SettingsDock(eeg_dock.layout)
        eeg_dock.dock_area.addDock(settings_dock.dock)

        eeg_inner_dock = MyDock('Part EEG', hide_title=True)
        eeg_dock.dock_area.addDock(eeg_inner_dock)

        for i in range(8):
            eeg_inner_dock.dock_area.addDock(
                    PlotDockWidget(
                            name='Input Signal',
                            plot=ScrollPlotWidget(
                                signals=[self._model.pipeline.signal_collector.input[i],
                                         self._model.pipeline.filter_stage.output[i]])))

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

