# --My Packages--
# from V2.GUI.tabs.live_graph_tab.view.live_graph_tab_view import LiveGraphTabView
# from V2.GUI.tabs.model.model import Model


class EegPlotsDockConnector:
    def __init__(self, view, model):
    # def __init__(self, view: LiveGraphTabView, model: Model):
        self._view = view
        self._model = model

        self._init_variables(view, model)
        self._connect_start_btn()

    def _init_variables(self, view, model):
        self.plot_dock_list = view.eeg_dock.plots_dock.plot_dock_list
        self.settings = view.eeg_dock.settings_dock
        self.start_btn = view.eeg_dock.settings_dock.start_btn
        self.time_dock = view.eeg_dock.plots_dock.time_dock
        self.signal_collector = model.pipeline.signal_collector

    def _connect_start_btn(self):
        self.start_btn.clicked.connect(self._connect)

    def _connect(self):
        self._model.pipeline.start()
        self._connect_plots()
        self._connect_other_plots()
        self._connect_time_plot()

    def _connect_plots(self):
        for ch in range(self._model.N_CH):
            self._connect_plots_signals(ch)
            self._connect_plots_timers(ch)
            self._connect_plots_events_pos(ch)

    def _connect_plots_timers(self, ch):
        self.plot_dock_list[ch].plot.connect_timers()

    def _connect_plots_signals(self, ch):
        signals = [
                   self.signal_collector.input[ch],
                   # self._model.pipeline.signal_collector.input[0],
                   self._model.pipeline.filter_stage.output[ch]
                  ]
        # TODO: ALEXM: pass signal in parameter instead ?
        self.plot_dock_list[ch].plot.connect_signals(signals)

    def _connect_plots_events_pos(self, ch):
        self.plot_dock_list[ch].plot.connect_events_pos(
            self._model.pipeline.signal_collector.events_pos)

    # ----- TODO: ALEXM: éviter cette répétition ----
    def _connect_other_plots(self):
        for ch in range(self._model.N_CH):
            all_signals_list = [
                # [self.signal_collector.experiments],
                # [self._model.pipeline.filter_stage.output[ch]],
                # [self.signal_collector.input[ch]],
                # [self.signal_collector.input[ch], self._model.pipeline.filter_stage.output[ch]],
                # [self.signal_collector.timestamps]
            ]
            for signal_no, signals_list in enumerate(all_signals_list):
                self._add_other_plot(ch)
                self._connect_other_plots_signals(ch, signal_no, signals_list)
                self._connect_other_plots_timers(ch, signal_no)

    def _add_other_plot(self, ch):
        self.plot_dock_list[ch].add_other_plot()

    def _connect_other_plots_timers(self, ch, signal_no):
        self.plot_dock_list[ch].other_plots[signal_no].connect_timers()

    def _connect_other_plots_signals(self, ch, signal_no, signals_list):
        self.plot_dock_list[ch].other_plots[signal_no].connect_signals(signals_list)
    # --------------------------------------------------

    def _connect_time_plot(self):
        self.time_dock.plot.curr_time = self.signal_collector.timestamps
        self.time_dock.plot.timer.start(0)

