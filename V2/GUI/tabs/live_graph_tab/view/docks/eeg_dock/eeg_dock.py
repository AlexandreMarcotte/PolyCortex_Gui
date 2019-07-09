# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_settings_dock import EegSettingsDock
from ..eeg_dock.inner_docks.eeg_plots_dock import EegPlotsDock


class EegDock(InnerDock):
    def __init__(self):
        super().__init__(
                name='EEG dock',
            toggle_btn=False, add_dock_area=True,
                set_scroll=True, hide_title=False)
        self.settings_dock = self._init_settings_inner_dock()
        self.plots_dock = self._init_eeg_plots_dock()
        # self.inner_docks = {'settings_dock': EegSettingsDock(self.layout),
        #                     'plots_dock': EegPlotsDock()}
        # self._init_all_inner_dock()

    # def _init_all_inner_dock(self):
    #     for key, val in self.inner_docks.items():
    #         self.__dict__[key] = val
    #         self.dock_area.addDock(self.__dict__[key].dock)

    def _init_settings_inner_dock(self):
        settings_dock = EegSettingsDock(self.layout)
        self.dock_area.addDock(settings_dock.dock)
        return settings_dock

    def _init_eeg_plots_dock(self):
        plots_dock = EegPlotsDock()
        self.dock_area.addDock(plots_dock.dock)
        return plots_dock

    # def _init_other_dock(self):
    #     self.dock.area.addDock(PlotDock(
    #             name='Spectogram',
    #             plot=SpectogramPlotWidget(
    #                 signals=[self._model.pipeline.fft_stage.output])))
