from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.main_dock import MainDock
# FFT
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.fft_settings_dock import FftSettingsDock
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
# EEG
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_settings_dock import EegSettingsDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_plots_dock import EegPlotsDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.saving_dock import SavingDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.banner_dock import BannerDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.write_to_hardware_dock import WriteHardwareDock
# Viz 3D
from V2.GUI.tabs.live_graph_tab.view.docks.visualization_3d_dock.inner_docks.visualization_3d_settings_dock import Visualisation3dSettingsDock
from V2.GUI.tabs.live_graph_tab.view.docks.visualization_3d_dock.inner_docks.plot.visualization_3d_plot_dock import Visualization3dPlotsDock


class View(QWidget):
    def __init__(self):
        super().__init__()

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self._init_docks()

    def _init_docks(self):
        self._init_eeg_dock()
        self._init_fft_dock()
        self._init_visualization_3D_dock()

    def _init_eeg_dock(self):
        self.eeg_dock = MainDock(name='EEG',
            settings_dock=EegSettingsDock, plot_dock=EegPlotsDock())
        # Saving dock
        self.saving_dock = SavingDock(external_layout=self.eeg_dock.inner_layout)
        self.eeg_dock.add_dock(self.saving_dock, 'top', self.eeg_dock.plot_dock)
        # Banner dock
        self.banner_dock = BannerDock(external_layout=self.eeg_dock.inner_layout)
        self.eeg_dock.add_dock(self.banner_dock, 'top', self.eeg_dock.plot_dock)
        self.banner_dock.hide()
        # Write harware dock
        self.write_hardware_dock = WriteHardwareDock(
            external_layout=self.eeg_dock.inner_layout)
        self.eeg_dock.add_dock(
            self.write_hardware_dock, 'top', self.eeg_dock.plot_dock)

        self.area.addDock(self.eeg_dock)

    def _init_fft_dock(self):
        self.fft_dock = MainDock(name='FFT',
            settings_dock=FftSettingsDock, plot_dock=PlotDock(curve_color='b'))
        self.area.addDock(self.fft_dock, 'right', self.eeg_dock)

    def _init_visualization_3D_dock(self):
        self.visualization_3D_dock = MainDock(name='Visualization 3D',
            settings_dock=Visualisation3dSettingsDock,
            plot_dock=Visualization3dPlotsDock())
        self.area.addDock(self.visualization_3D_dock, 'bottom', self.fft_dock)




        # fft_dock = EegDock()
        # self.area.addDock(fft_dock, 'right', self.eeg_dock)
        # return fft_dock

        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Filter Sig out & in',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.filter_stage.output,
        #                  self._model.pipeline.filter_stage.input])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Timestamp',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.signal_collector.timestamps])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='FFT',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Spectogram',
        #     plot=SpectogramPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))

