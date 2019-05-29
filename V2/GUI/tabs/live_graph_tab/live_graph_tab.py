from pyqtgraph.dockarea import *
from V2.GUI.tabs.live_graph_tab.plot_dock_widget import PlotDockWidget
from V2.pipeline.pipeline import Pipeline
from PyQt5.QtWidgets import *


class LiveGraphTab(QWidget):
    def __init__(self):
        super().__init__()
        # Start pipeline
        self.pipeline = Pipeline()

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        # Init docks
        self.init_dock('Input Signal',
                       [self.pipeline.signal_collector.input])
        self.init_dock('Filter Sig out & in',
                       [self.pipeline.filter_stage.output,
                        self.pipeline.filter_stage.input])
        self.init_dock('Filtered Signal input',
                       [self.pipeline.filter_stage.input])
        self.init_dock('Timestamp',
                       [self.pipeline.signal_collector.timestamps])
        self.init_dock('FFT',
                       [self.pipeline.fft_stage.output])
        self.init_dock('Spectrogram',
                       [self.pipeline.fft_stage.output], plot_type='2D')

    def init_dock(self, name, signals, plot_type='1D'):
        dock = PlotDockWidget(name, signals=signals, plot_type=plot_type)
        self.area.addDock(dock)
        return dock

