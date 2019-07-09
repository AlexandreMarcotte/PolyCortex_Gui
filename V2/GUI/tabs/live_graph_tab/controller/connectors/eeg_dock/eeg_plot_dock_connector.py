class EegPlotsDockConnector:
    def __init__(self, n_ch, view, model):
        self._n_ch = n_ch
        self._view = view
        self._model = model

        self.plot_dock = self._view.eeg_dock.plots_dock.plot_docks

    def connect(self):
        for ch in range(self._n_ch):
            self._connect_toggle_btn(ch)
            self._connect_control_btn(ch)
            self.connect_plots(ch)

    def _connect_toggle_btn(self, ch):
        self.plot_dock[ch].toggle_btn.clicked.connect(
                self.plot_dock[ch].scroll_plot.toggle_timer)

    def _connect_control_btn(self, ch):
        # Avg val btn
        avg_val_btn = self.plot_dock[ch].avg_value_btn
        avg_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        avg_val_btn.clicked.connect(avg_val_btn.show_action)
        # Max val btn
        max_val_btn = self.plot_dock[ch].max_value_btn
        max_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        max_val_btn.clicked.connect(max_val_btn.show_action)

    def connect_plots(self, ch):
        signals = [self._model.pipeline.signal_collector.input[ch]]
        self.plot_dock[ch].scroll_plot.connect_signals(signals)
                   # self._model.pipeline.filter_stage.output[ch]]
        # if ch == 0:
        #     signals = [self._model.pipeline.fft_stage.input[0]]

