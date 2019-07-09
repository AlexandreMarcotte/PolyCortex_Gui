# --My packages--
from V2.GUI.tabs.live_graph_tab.model.model import Model
from V2.GUI.tabs.live_graph_tab.view.view import View
# EEG
from V2.GUI.tabs.live_graph_tab.controller.connectors.eeg_dock.setting_dock_connector import SettingDockConnector
from V2.GUI.tabs.live_graph_tab.controller.connectors.eeg_dock.eeg_plot_dock_connector import EegPlotsDockConnector
# FFT
from V2.GUI.tabs.live_graph_tab.controller.connectors.eeg_dock.setting_dock_connector import SettingDockConnector
from V2.GUI.tabs.live_graph_tab.controller.connectors.fft_dock.fft_plot_dock_connector import FftPlotsDockConnector


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View()

        self.N_CH = 8
        self._connect()

    def _connect(self):
        self._connect_eeg_dock()
        self._connect_ftt_dock()
        
    def _connect_eeg_dock(self):
        SettingDockConnector(self.N_CH, self._view).connect()
        EegPlotsDockConnector(self.N_CH, self._view, self._model).connect()

    def _connect_ftt_dock(self):
        # SettingDockConnector(self._view).connect()
        FftPlotsDockConnector(self._view, self._model).connect()
