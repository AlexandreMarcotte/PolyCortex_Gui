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

        self._init_variables(view, model)
        self._connect_start_btn()

    def _init_variables(self, view, model):
        self.plots = view.eeg_dock.plots_dock.plot_dock_list
        self.settings = view.eeg_dock.settings_dock
        self.start_btn = view.eeg_dock.settings_dock.start_btn
        self.time_dock = view.eeg_dock.plots_dock.time_dock
        self.signal_collector = model.pipeline.signal_collector

    def _connect_start_btn(self):
        self.start_btn.clicked.connect(self._connect)

    def _connect(self):
        self._model.pipeline.start()
        self._connect_plots()
        self._connect_time_plot()

    def _connect_time_plot(self):
        self.time_dock.plot.curr_time = self.signal_collector.timestamps
        self.time_dock.plot.timer.start(0)

    def _connect_plots(self):
        for ch in range(self._model.N_CH):
            self._connect_plots_timers(ch)
            self._connect_plots_signals(ch)

    def _connect_plots_timers(self, ch):
        self.plots[ch].plot.connect_timers()

    def _connect_plots_signals(self, ch):
        signals = [self.signal_collector.input[ch],
                   # self._model.pipeline.signal_collector.input[0]]
                   self._model.pipeline.filter_stage.output[ch]]
        # TODO: ALEXM: pass signal in parameter instead ?
        self.plots[ch].plot.connect_signals(signals)


