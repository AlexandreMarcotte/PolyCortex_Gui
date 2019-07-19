from functools import partial
from V2.GUI.tabs.live_graph_tab.model.model import Model
# from V2.GUI.tabs.live_graph_tab.view.view import View


class EegSettingsDockConnector:
    def __init__(self, view, model):
            # def __init__(self, view: View, model: Model):
            self._view = view
            self._model = model

            self.plots = self._view.eeg_dock.plots_dock.plot_dock_list
            self.settings = self._view.eeg_dock.settings_dock
            self.start_btn = self._view.eeg_dock.settings_dock.start_btn
            self.time_dock = self._view.eeg_dock.plots_dock.time_dock

            self._connect_start_btn()

    def _connect(self):
        for ch in range(self._model.N_CH):
            self._connect_toggle_btn(ch)
            self._connect_axis(
                plot=self.plots[ch].plot, cb=self.settings.horizontal_scale_cb,
                axis='x')  #FIX so that the second conversion is done
            self._connect_axis(
                plot=self.plots[ch].plot, cb=self.settings.vertical_scale_cb,
                axis='y')
        self.connect_pins_settings_btn()

    def _connect_start_btn(self):
        self.start_btn.clicked.connect(self._connect)

    def _connect_axis(self, plot, cb, axis='x'):
        scale_axis = plot.scale_axis
        cb.activated[str].connect(partial(scale_axis, axis=axis))

    def _connect_toggle_btn(self, ch):
        self.plots[ch].toggle_btn.clicked.connect(
            self.plots[ch].plot.toggle_timer)

    def connect_pins_settings_btn(self):
        self._view.eeg_dock.pins_settings_btn.clicked.connect(
            self._view.eeg_dock.plots_dock.hide_pins_settings)


