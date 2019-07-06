from PyQt5.QtWidgets import *
# --My packages--
from .model import Model
from .view import View


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View(self._model)

    def connect(self):

        pass
        # self._view.eeg_dock..activated[str].connect(conn_func)

    def connect_plots(self):
        for i in range(8):
            # self._view.eeg_dock.plot_docks[i].scroll_plot.
            signals = [self._model.pipeline.signal_collector.input[i],
                       self._model.pipeline.filter_stage.output[i]]

