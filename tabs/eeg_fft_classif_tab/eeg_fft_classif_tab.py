# -*- coding: utf-8 -*-
# -- General packages --
## Graph the data
from PyQt5.QtWidgets import *

import pyqtgraph as pg
from pyqtgraph.dockarea import *

# -- My packages --
## Graphes
from .eeg_graph import EegPlotsCreator
from .wave_graph import WaveGraph
from .fft_graph import FftGraph
from .classification_graph import ClassifPlotCreator
from .banner import add_banner

from save.save_to_file import DataSaver

from app.colors import *


class EegFftClassifTab:
    def __init__(self, main_window, tab_w, gv):
        super().__init__()
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv
        # self.gv.n_data_created = n_data_created
        self.gv.N_CH = len(self.gv.data_queue)

        self.create_layout()
        self.create_docks()
        self.create_tab()

    def create_layout(self):
        self.tab_w.layout = QHBoxLayout(self.main_window)
        # Add docs to the tab
        self.area = DockArea()
        self.tab_w.layout.addWidget(self.area)

    def create_docks(self):
        # - EEG
        self.eeg_layout, eeg_dock = self.create_eeg_layout()
        # - FFT
        self.fft_layout, fft_dock = self.create_fft_layout()
        # - Wave plot
        self.wave_layout, wave_dock = self.create_wave_layout()
        # - Acceleration Dock
        self.show_classif_dock = Dock('Classification', size=(5, 10))
        self.area.addDock(self.show_classif_dock, 'below', self.wave_dock)
        self.classif_layout = pg.LayoutWidget()
        self.show_classif_dock.addWidget(self.classif_layout)
        # Make sure the wave is shown on top
        self.area.moveDock(self.wave_dock, 'above', self.show_classif_dock)
        # - Saving dock
        self.saving_dock = Dock('Saving', size=(1,1))
        self.saving_dock.hideTitleBar()
        self.area.addDock(self.saving_dock, 'bottom', eeg_dock)
        self.saving_layout = pg.LayoutWidget()
        self.saving_dock.addWidget(self.saving_layout)
        # - Banner dock
        self.banner_dock = Dock('Banner', size=(1, 1))
        self.banner_dock.hideTitleBar()
        self.area.addDock(self.banner_dock, 'bottom', self.wave_dock)
        self.banner_layout = pg.LayoutWidget()
        self.banner_dock.addWidget(self.banner_layout)

    def create_eeg_layout(self):
        # - EEG
        eeg_dock = Dock('EEG')
        self.area.addDock(eeg_dock, 'left')
        # Add the layout to the dock
        eeg_layout = pg.LayoutWidget()
        # Create scrolling region for portion graph
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        eeg_dock.addWidget(scroll)
        scroll.setWidget(eeg_layout)
        return eeg_layout, eeg_dock

    def create_fft_layout(self):
        fft_dock = Dock('FFT', size=(5,10))
        self.area.addDock(fft_dock, 'right')
        fft_layout = pg.LayoutWidget()
        fft_dock.addWidget(fft_layout)
        return fft_layout, fft_dock

    def create_wave_layout(self):
        wave_dock = Dock('Wave', size=(5,10))
        self.area.addDock(wave_dock, 'bottom', fft_dock)
        wave_layout = pg.LayoutWidget()
        wave_dock.addWidget(wave_layout)

    def create_layout(self, dock_name, pos_from=None, scroll=None):
        dock = Dock(dock_name)
        if pos_from:
            self.area.addDock(dock, pos, pos_from)
        else:
            self.area.addDock(dock, pos)
        layout = pg.LayoutWidget()
        if scroll:
            dock.addWidget(scroll)
        dock.addWidget()



    def create_tab(self):
        data_saver = DataSaver(self.main_window, self.saving_layout)
        # Create the plots
        # - EEG
        self.eeg_plot_creator = EegPlotsCreator(
            self.gv, self.eeg_layout, data_saver)
        # - FFT
        FftGraph(self.main_window, self.fft_layout, self.gv)
        # - Wave plot
        WaveGraph(self.gv, self.main_window, self.wave_layout)
        # - Classif plot
        self.classif_plot_creator = ClassifPlotCreator(
            self.gv, self.classif_layout)
        # EEG actions
        add_banner(self.main_window, self.banner_layout)

        self.tab_w.setLayout(self.tab_w.layout)



