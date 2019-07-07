from PyQt5.QtWidgets import *
# --My packages--
from .model import Model
from .view import View


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View(self._model)

        self.connect()

    def connect(self):
        self.connect_plots()
        self.connect_settings_cb()

    def print_shit(self, txt):
        print(txt)

    def connect_settings_cb(self):
        self._view.eeg_dock.settings_dock.vertical_scale_cb.connect_cb(
            self.print_shit)
        self._view.eeg_dock.settings_dock.horizontal_scale_cb.connect_cb(
            self.print_shit)

    def connect_plots(self):
        for i in range(8):
            plots = self._view.eeg_dock.eeg_plots_dock.plot_docks[i].scroll_plot
            signals = [self._model.pipeline.signal_collector.input[i],
                       self._model.pipeline.filter_stage.output[i]]
            plots.connect_signals(signals)

