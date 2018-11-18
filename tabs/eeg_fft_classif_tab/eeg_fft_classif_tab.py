# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *

import pyqtgraph as pg
from pyqtgraph.dockarea import *

# -- My packages --
## Graphes
from .dock.eeg_dock.eeg_plots_creator import EegPlotsCreator
from .dock.wave_dock.wave_graph import WaveGraph
from .dock.fft_dock.fft_graph import FftGraph
from .dock.classif_dock.classification_plot_creator import ClassifPlotCreator
from .dock.banner_dock.banner import add_banner

from save.save_to_file import DataSaver
from app.colors import *
from tabs.region import Regions


class EegFftClassifTab(QWidget):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv

        self.init_tab_w()
        self.init_docks()
        self.create_tab()

    def init_tab_w(self):
        self.layout = QHBoxLayout(self)
        # Add docs to the tab
        self.area = DockArea()
        self.layout.addWidget(self.area)

    def init_docks(self):
        # - EEG
        self.eeg_layout, eeg_dock = self.create_layout(
            'EEG', 'left', size=(5, 15), scroll=True)
        # - FFT
        self.fft_layout, fft_dock = self.create_layout(
            'FFT', 'right', size=(5, 10))
        # - Wave plot
        self.wave_layout, wave_dock = self.create_layout(
            'Wave', 'bottom', fft_dock, size=(5, 10))
        # - Acceleration Dock
        self.classif_layout, classif_dock = self.create_layout(
            'Classification', 'below', wave_dock, size=(5, 10))
        # - Banner dock
        self.banner_layout, banner_dock = self.create_layout(
            'Banner', 'bottom', eeg_dock)
        # - Saving dock
        self.saving_layout, saving_dock = self.create_layout(
            'Saving', 'below', banner_dock)

    def create_layout(self, dock_name, pos, related_dock=None, size=(1, 1),
                      hide_title=False, scroll=False):
        dock = Dock(dock_name, size=size)
        self.area.addDock(dock, pos, related_dock)
        layout = pg.LayoutWidget()
        if scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            dock.addWidget(scroll)
            scroll.setWidget(layout)
        else:
            dock.addWidget(layout)
        if hide_title:
            dock.hideTitleBar()
        return layout, dock

    def create_tab(self):
        # Regions
        data_saver = DataSaver(self, self.saving_layout)
        # Create the graphes inside the each dock layout
        eeg_plot_creator = EegPlotsCreator(self.gv, self.eeg_layout, data_saver)
        x = eeg_plot_creator.regions
        FftGraph(self.gv, self.fft_layout)
        WaveGraph(self.gv, self.wave_layout)
        ClassifPlotCreator(self.gv, self.classif_layout)
        add_banner(self.banner_layout)

        self.setLayout(self.layout)