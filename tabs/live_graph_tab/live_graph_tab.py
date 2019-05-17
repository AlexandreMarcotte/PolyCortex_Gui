# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import *
# -- My packages --
## Graphes
from .dock.eeg_dock.eeg_plots_creator import MainEegDock
from .dock.power_band_dock.power_band_graph import PowerBandGraph
from .dock.power_band_over_time_dock.power_band_over_time_graph import \
        PowerBandGraphOverTime
from .dock.fft_dock.fft_dock import FftDock
from .dock.classif_dock.classification_plot_creator import ClassifPlotCreator
from .dock.viz_3D_dock.viz_3D import Viz3D
from .dock.spectogram3d_dock.Spectogram3D import Spectogram3D
from .dock.spectogram_dock.Spectogram import Spectogram
from .dock_handler import DockHandler


class LiveGraphTab(QWidget):
    def __init__(self, gv, parent):
        super().__init__()
        self.gv = gv
        self.gv.set_main_window(self)
        self.parent = parent

        self.init_tab_w()
        self.docks_menu = self.create_docks_menu()
        self.init_dock_layout()

    def init_tab_w(self):
        self.layout = QHBoxLayout(self)
        self.area = DockArea()
        self.layout.addWidget(self.area)

    def create_docks_menu(self):
        docks_menu = self.parent.menu_bar.main_menu.addMenu(
                'Add or Remove Dock')
        self.parent.menu_bar.main_menu.addMenu(docks_menu)
        return docks_menu

    def init_dock_layout(self):
        self.eeg = DockHandler(
                'EEG', self, self.docks_menu, MainEegDock, [self.gv],
                'left', size=(6, 10), scroll=True)

        self.fft = DockHandler(
                'FFT', self, self.docks_menu, FftDock, [self.gv], 'right',
                size=(5, 10), scroll=True)

        self.power_band = DockHandler(
                'Power band', self, self.docks_menu, PowerBandGraph, [self.gv],
                'below', self.fft.dock, size=(5, 10), scroll=True)

        self.power_band_over_time = DockHandler(
                'Power band over time', self, self.docks_menu,
                PowerBandGraphOverTime, [self.gv], 'below', self.fft.dock,
                size=(5, 10), scroll=True)

        self.Spectogram3D = DockHandler(
                'Spectogram 3D', self, self.docks_menu, Spectogram3D,
                [self.gv], 'below', self.fft.dock, size=(5, 10), scroll=True)

        self.fft_over_time_2D = DockHandler(
                'Spectogram', self, self.docks_menu, Spectogram, [self.gv],
                'below', self.fft.dock, size=(5, 10), scroll=True)

        self.classification = DockHandler(
                'Classification', self, self.docks_menu, ClassifPlotCreator,
                [self.gv], 'bottom', self.fft.dock, size=(5, 10), scroll=True)

        self.visualization3D = DockHandler(
                'Visualization 3D', self, self.docks_menu, Viz3D, [self.gv],
                'below', self.classification.dock, scroll=True)

        self.fft.dock.raiseDock()

        self.setLayout(self.layout)



