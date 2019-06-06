from pyqtgraph.dockarea import *
from .plot_dock_widget import PlotDockWidget
from V2.pipeline.pipeline import Pipeline
from PyQt5.QtWidgets import *
# --My packages--
from .plot_widgets.scroll_plot_widget import ScrollPlotWidget
from .plot_widgets.spectrogram_plot_widget import SpectogramPlotWidget


class LiveGraphTab(QWidget):
    def __init__(self):
        super().__init__()
        # Start pipeline
        self.pipeline = Pipeline()

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self.init_docks()

    def init_docks(self):
        self.area.addDock(PlotDockWidget(name='Input Signal',
            plot=ScrollPlotWidget(
                signals=[self.pipeline.signal_collector.input])))

        self.area.addDock(PlotDockWidget(
            name='Filter Sig out & in',
            plot=ScrollPlotWidget(
                signals=[self.pipeline.filter_stage.output,
                         self.pipeline.filter_stage.input])))

        self.area.addDock(PlotDockWidget(
            name='Timestamp',   
            plot=ScrollPlotWidget(
                signals=[self.pipeline.signal_collector.timestamps])))

        self.area.addDock(PlotDockWidget(
            name='FFT',
            plot=ScrollPlotWidget(
                signals=[self.pipeline.fft_stage.output])))

        self.area.addDock(PlotDockWidget(
            name='Spectogram',
            plot=SpectogramPlotWidget(
                signals=[self.pipeline.fft_stage.output])))
