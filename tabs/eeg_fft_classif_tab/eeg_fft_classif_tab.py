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
from .dock.banner_dock.banner import Banner
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
        self.menu_docks = self.parent.main_menu.addMenu('Docks')
        self.parent.main_menu.addMenu(self.menu_docks)
        self.init_dock_layout()

    def init_tab_w(self):
        self.layout = QHBoxLayout(self)
        self.area = DockArea()
        self.layout.addWidget(self.area)

    def init_dock_layout(self):
        # - EEG
        self.create_layout('EEG', EegPlotsCreator, [self.gv], 'left',
                           size=(6, 10), scroll=True)
        # - FFT
        self.create_layout('FFT', FftGraph, [self.gv], 'right',
                           size=(5, 10))
        # - Wave plot
        self.create_layout('Wave', WaveGraph, [self.gv], 'bottom',
                           self.FFT.dock, size=(5, 10))
        # - Acceleration Dock
        self.create_layout('Classification', ClassifPlotCreator, [self.gv],
                           'below', self.Wave.dock, size=(5, 10))
        # - Banner dock
        self.create_layout('Banner', Banner, [], 'bottom', self.EEG.dock)
        # - Saving dock
        self.create_layout('Saving', DataSaver, [self, self.gv], 'below',
                           self.Banner.dock)
        self.EEG.dock_obj.set_saver(self.Saving.dock_obj)
        # - Viz 3D dock
        self.create_layout('Visualization3D', Viz3D, [self.gv], 'below',
                           self.Classification.dock)

        self.setLayout(self.layout)

    def create_layout(self, dock_name, dock_obj, param, pos, related_dock=None, size=(1, 1),
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

        param.append(layout)
        exec(f'''self.{dock_name} = DockHandler(dock_name, self, self.menu_docks, dock, dock_obj, param)''')


class DockHandler:
    def __init__(self, name, mainwindow, menu, dock, DockObj, param):
        self.name = name
        self.mainwindow = mainwindow
        self.dock = dock

        self.dock_obj = DockObj(*param)
        if name == 'EEG':
            x = self.dock_obj.regions

        self.state = 'checked'

        self.check_actn = QtGui.QAction(name, mainwindow, checkable=True)
        self.check_actn.setChecked(True)
        self.check_actn.triggered.connect(self.open_close_dock)
        self.check_actn.setStatusTip(f'Check {name} to open this dock...')

        menu.addAction(self.check_actn)

    def open_close_dock(self):
        print('My name is: ', self.name)
        if self.state == 'checked':
            self.dock.close()
            self.state = 'unchecked'


