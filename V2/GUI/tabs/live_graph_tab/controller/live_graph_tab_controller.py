from PyQt5.QtWidgets import *
# --My packages--
from V2.GUI.tabs.live_graph_tab.model.model import Model
from V2.GUI.tabs.live_graph_tab.view.view import View
from .connectors.setting_dock_connector import SettingDockConnector


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View(self._model)

        self.connect()

    def connect(self):
        self.connect_plots()
        SettingDockConnector(self._view).connect()
        self.connect_plot_dock_btn()

    def connect_plot_dock_btn(self):
        for ch in range(8):
            plot_dock = self._view.eeg_dock.eeg_plots_dock.plot_docks[ch]
            plot_dock.activation_btn.clicked.connect(
                    plot_dock.scroll_plot.toggle_timer)

    def connect_settings_dock(self):
        # v axis
        settings_dock = self._view.eeg_dock.settings_dock
        for ch in range(8):
            scale_v_axis = self._view.eeg_dock.eeg_plots_dock.plot_docks[ch].scroll_plot.scale_y_axis
            settings_dock.vertical_scale_cb.connect_cb(scale_v_axis)
        # horizontal axis
        settings_dock.horizontal_scale_cb.connect_cb( self.print_shit)

    def print_shit(self):
        print('shittt')

    def connect_plots(self):
        for i in range(8):
            plots = self._view.eeg_dock.eeg_plots_dock.plot_docks[i].scroll_plot
            signals = [self._model.pipeline.signal_collector.input[i],
                       self._model.pipeline.filter_stage.output[i]]
            plots.connect_signals(signals)

