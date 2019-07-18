# --General Packages--
from functools import partial
# --My Packages--
from V2.GUI.tabs.live_graph_tab.model.model import Model
# from V2.GUI.tabs.live_graph_tab.view.view import View


class EegPlotsDockConnector:
    def __init__(self, view, model):
    # def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.plots = self._view.eeg_dock.plots_dock.plot_dock_list
        self.settings = self._view.eeg_dock.settings_dock
        self.start_btn = self._view.eeg_dock.settings_dock.start_btn
        self.time_dock = self._view.eeg_dock.plots_dock.time_dock

        self._connect_start_btn()

    def _connect_start_btn(self):
        self.start_btn.clicked.connect(self._connect)

    def _connect(self):
        self._model.pipeline.start()
        for ch in range(self._model.N_CH):
            self.plots[ch].plot.connect_timers()
            self.connect_plots(ch)

        self.connect_pins_settings_btn()
        self.time_dock.plot.curr_time = \
            self._model.pipeline.signal_collector.timestamps
        self.time_dock.plot.timer.start(0)

    def connect_plots(self, ch):
        signals = [self._model.pipeline.signal_collector.input[ch],
                   # self._model.pipeline.signal_collector.input[0]]
                   self._model.pipeline.filter_stage.output[ch]]
        # TODO: ALEXM: pass signal in parameter instead ?
        self.plots[ch].plot.connect_signals(signals)

    def connect_pins_settings_btn(self):
        self._view.eeg_dock.pins_settings_btn.clicked.connect(
            self._view.eeg_dock.plots_dock.hide_pins_settings)
