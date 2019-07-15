from functools import partial


class EegPlotsDockConnector:
    def __init__(self, n_ch, view, model):
        self._n_ch = n_ch
        self._view = view
        self._model = model

        self.plots = self._view.eeg_dock.plots_dock.plot_dock_list
        self.settings = self._view.eeg_dock.settings_dock

    def connect(self):
        for ch in range(self._n_ch):
            self._connect_toggle_btn(ch)
            self._connect_control_btns(ch)
            self.connect_plots(ch)
            self._connect_start_btn(ch)
            # self._connect_axis(
            #     plot=self.plots[ch].plot, cb=self.settings.horizontal_scale_cb,
            #     axis='x')   FIX so that the second conversion is done
            self._connect_axis(
                plot=self.plots[ch].plot, cb=self.settings.vertical_scale_cb,
                axis='y')

        self.connect_pins_settings_btn()
        self._view.eeg_dock.plots_dock.time_dock.plot.curr_time = \
            self._model.pipeline.signal_collector.timestamps
        self._view.eeg_dock.plots_dock.time_dock.plot.timer.start(0)

    def _connect_axis(self, plot, cb, axis='x'):
        # connect function
        scale_axis = plot.scale_axis
        cb.activated[str].connect(partial(scale_axis, axis=axis))

    def _connect_start_btn(self, ch):
        if ch == 0:
            # Start pipeline
            self._model.pipeline.streamer.start()
            self._model.pipeline.fft_stage.start()
        self._view.eeg_dock.settings_dock.start_btn.clicked.connect(
            self.plots[ch].plot.connect_timers)

    def _connect_toggle_btn(self, ch):
        self.plots[ch].toggle_btn.clicked.connect(
                self.plots[ch].plot.toggle_timer)

    def _connect_control_btns(self, ch):
        # Avg val btn
        avg_val_btn = self.plots[ch].avg_value_btn
        avg_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        # avg_val_btn.clicked.connect(avg_val_btn.show_action)
        # Max val btn
        max_val_btn = self.plots[ch].max_value_btn
        max_val_btn.data_queue = self._model.pipeline.signal_collector.input[ch]
        # max_val_btn.clicked.connect(max_val_btn.show_action)

    def connect_plots(self, ch):
        signals = [self._model.pipeline.signal_collector.input[ch]]
        self.plots[ch].plot.connect_signals(signals)

    def connect_pins_settings_btn(self):
        self._view.eeg_dock.pins_settings_btn.clicked.connect(
            self._view.eeg_dock.plots_dock.hide_pins_settings)
