from functools import partial


# from V2.GUI.tabs.live_graph_tab.view.live_graph_tab_view import LiveGraphTabView
from V2.GUI.tabs.model.model import Model


class EegSettingsDockConnector:
    def __init__(self, view, model):
    # def __init__(self, view: LiveGraphTabView, model: Model):
        self._view = view
        self._model = model

        self.plots = self._view.eeg_dock.plots_dock.plot_dock_list
        self.settings = self._view.eeg_dock.settings_dock
        self.start_btn = self._view.eeg_dock.settings_dock.start_btn
        self.time_dock = self._view.eeg_dock.plots_dock.time_dock
        self.data_saver = self._view.eeg_dock.saving_dock.data_saver

        self._connect_start_btn()

    def _connect_start_btn(self):
        self.start_btn.clicked.connect(self._connect)

    def _connect(self):
        for ch in range(self._model.N_CH):
            self._connect_toggle_btn(ch)
            self._connect_axis(
                plot=self.plots[ch].plot, cb=self.settings.horizontal_scale_cb,
                axis='x')  #FIX so that the second conversion is done
            self._connect_axis(
                plot=self.plots[ch].plot, cb=self.settings.vertical_scale_cb,
                axis='y')
            self._connect_color_buttons(ch)
        self.connect_pins_settings_btn()
        self._connect_save_data_now_btn()

    def _connect_axis(self, plot, cb, axis='x'):
        scale_axis = plot.scale_axis
        cb.activated[str].connect(partial(scale_axis, axis=axis, symetric=True))

    def _connect_toggle_btn(self, ch):
        self.plots[ch].toggle_btn.clicked.connect(
            self.plots[ch].plot.toggle_timer)

    def connect_pins_settings_btn(self):
        self._view.eeg_dock.pins_settings_btn.clicked.connect(
            self._view.eeg_dock.plots_dock.hide_pins_settings)

    def _connect_color_buttons(self, ch): # TODO: ALEXM: Avoid repetition
        # EEG
        self.plots[ch].color_btn.sigColorChanged.connect(
            self.plots[ch].toggle_btn.change_color)
        self.plots[ch].color_btn.sigColorChanged.connect(
            self.plots[ch].plot.change_curves_color)
        # FFT
        self.plots[ch].color_btn.sigColorChanged.connect(
            partial(self._view.fft_dock.plot_dock.plot.change_curves_color, ch))

    def _connect_save_data_now_btn(self):
        self.data_saver.connect_save_data_now_btn(
            self._model.pipeline.signal_collector.long_term_memory.dump_memory_into_file)



