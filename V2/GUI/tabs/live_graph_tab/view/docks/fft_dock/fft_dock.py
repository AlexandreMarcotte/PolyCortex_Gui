# --My packages--
from V2.utils.my_dock import MyDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_settings_dock import EegSettingsDock
from ..eeg_dock.inner_docks.eeg_plots_dock import EegPlotsDock
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.spectrogram_plot_widget import SpectogramPlotWidget
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


# class EegDock(MyDock):
#     def __init__(self):
#         super().__init__('FFT_dock')
#         self.settings_dock = self._init_settings_inner_dock()
#         self.eeg_plots_dock = self._init_eeg_plots_dock()
#
#     def _init_settings_inner_dock(self):
#         settings_dock = EegSettingsDock(self.layout)
#         self.dock_area.addDock(settings_dock.dock)
#         return settings_dock
#
#     def _init_eeg_plots_dock(self):
#         eeg_plots_dock = EegPlotsDock()
#         self.dock_area.addDock(eeg_plots_dock)
#         return eeg_plots_dock
#
