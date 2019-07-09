# --My packages--
from V2.GUI.tabs.live_graph_tab.model.model import Model
from V2.GUI.tabs.live_graph_tab.view.view import View
from .connectors.setting_dock_connector import SettingDockConnector
from .connectors.eeg_plot_dock_connector import EegPlotsDockConnector


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View()

        self.N_CH = 8
        self._connect()

    def _connect(self):
        self._connect_eeg_dock()
        
    def _connect_eeg_dock(self):
        SettingDockConnector(self.N_CH, self._view).connect()
        EegPlotsDockConnector(self.N_CH, self._view, self._model).connect()

