# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


import pyqtgraph as pg
from pyqtgraph.dockarea import *

# -- My packages --
## Graphes
from .dock.eeg_dock.eeg_plots_creator import EegPlotsCreator
from .dock.wave_dock.wave_graph import WaveGraph
from .dock.fft_dock.fft_graph import FftGraph
from .dock.classif_dock.classification_plot_creator import ClassifPlotCreator
from .dock.banner_dock.banner import add_banner
from .dock.Viz_3D_dock.viz_3D import Viz3D

from save.data_saver import DataSaver
from app.colors import *
from tabs.region import Regions


class EegFftClassifTab(QWidget):
    def __init__(self, gv, parent):
        super().__init__()
        self.gv = gv
        self.parent = parent

        self.init_tab_w()
        self.init_docks()
        self.add_content_to_docks()

        self.menu_dock = self.create_menu_docks(self.parent.main_menu)                     # TODO: Use return instead for these functions
        self.parent.main_menu.addMenu(self.menu_dock)

    def create_menu_docks(self, main_menu):
        menu_docks = main_menu.addMenu('Docks')
        docks = {'EEG': None, 'FFT': None, 'ShowVisualization3D': None,
                 'Classification': None, 'Banner': None, 'Saving': None}

        for dock in docks:
            exec(f'docks[dock] = self.{dock} = DockOption(dock, self, menu_docks)')
        return menu_docks

    def init_tab_w(self):
        self.layout = QHBoxLayout(self)
        # Add docs to the tab
        self.area = DockArea()
        self.layout.addWidget(self.area)

    def init_docks(self):
        # - EEG
        self.eeg_layout, eeg_dock = self.create_layout(
            'EEG', 'left', size=(6, 10), scroll=True)
        # - FFT
        self.fft_layout, self.fft_dock = self.create_layout(
            'FFT', 'right', size=(5, 10))
        # - Wave plot
        self.wave_layout, wave_dock = self.create_layout(
            'Wave', 'bottom', self.fft_dock, size=(5, 10))
        # - Acceleration Dock
        self.classif_layout, classif_dock = self.create_layout(
            'Classification', 'below', wave_dock, size=(5, 10))
        # - Banner dock
        self.banner_layout, banner_dock = self.create_layout(
            'Banner', 'bottom', eeg_dock)
        # - Saving dock
        self.saving_layout, saving_dock = self.create_layout(
            'Saving', 'below', banner_dock)
        # - Viz 3D dock
        self.viz_3D_layout, viz_3D_dock = self.create_layout(
            'Visualization 3D', 'below', classif_dock)

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

    def add_content_to_docks(self):
        # Regions
        data_saver = DataSaver(self, self.saving_layout, self.gv)
        # Create the graphes inside the each dock layout
        eeg_plot_creator = EegPlotsCreator(self.gv, self.eeg_layout, data_saver)
        x = eeg_plot_creator.regions
        FftGraph(self.gv, self.fft_layout)
        WaveGraph(self.gv, self.wave_layout)
        ClassifPlotCreator(self.gv, self.classif_layout)
        add_banner(self.banner_layout)
        Viz3D(self.gv, self.viz_3D_layout)

        self.setLayout(self.layout)


class DockOption:
    def __init__(self, name, mainwindow, menu):
        self.name = name

        self.check_actn = QtGui.QAction(name, mainwindow, checkable=True)
        self.check_actn.triggered.connect(self.print_func)
        self.check_actn.setStatusTip(f'Check {name} to open this dock...')

        menu.addAction(self.check_actn)

    def print_func(self):
        print('My name is: ', self.name)
