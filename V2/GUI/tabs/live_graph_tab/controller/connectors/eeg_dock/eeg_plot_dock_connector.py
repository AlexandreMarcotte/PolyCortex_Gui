class EegPlotsDockConnector:
    def __init__(self, n_ch, view, model):
        self._n_ch = n_ch
        self._view = view
        self._model = model

        self.plot_dock_list = self._view.eeg_dock.plots_dock.plot_dock_list

    def connect(self):
        for ch in range(self._n_ch):
            self._connect_toggle_btn(ch)
            self._connect_control_btns(ch)
            self.connect_plots(ch)
            self._connect_start_btn(ch)

        self.connect_pins_settings_btn()
        self._view.eeg_dock.plots_dock.time_dock.plot.curr_time = \
            self._model.pipeline.signal_collector.timestamps
        self._view.eeg_dock.plots_dock.time_dock.plot.timer.start(0)

    def _connect_start_btn(self, ch):
        if ch == 0:
            # Start pipeline
            self._model.pipeline.streamer.start()
            self._model.pipeline.fft_stage.start()
        self._view.eeg_dock.settings_dock.start_btn.clicked.connect(
            self.plot_dock_list[ch].plot.connect_timers)

    def _connect_toggle_btn(self, ch):
        self.plot_dock_list[ch].toggle_btn.clicked.connect(
                self.plot_dock_list[ch].plot.toggle_timer)

    def _connect_control_btns(self, ch):
        # Avg val btn
        avg_val_btn = self.plot_dock_list[ch].avg_value_btn
        avg_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        avg_val_btn.clicked.connect(avg_val_btn.show_action)
        # Max val btn
        max_val_btn = self.plot_dock_list[ch].max_value_btn
        max_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        max_val_btn.clicked.connect(max_val_btn.show_action)

    def connect_plots(self, ch):
        signals = [self._model.pipeline.signal_collector.input[ch]]
        self.plot_dock_list[ch].plot.connect_signals(signals)

    def connect_pins_settings_btn(self):
        self._view.eeg_dock.pins_settings_btn.clicked.connect(
            self._view.eeg_dock.plots_dock.hide_pins_settings)
