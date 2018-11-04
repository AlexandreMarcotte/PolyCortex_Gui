# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon
# from pyqtgraph.Qt import QtGui
import os
import numpy as np
from time import time

from functools import partial
# My packages
from app.global_variables import GlobVar
# -- Tabs --
from tabs.eeg_fft_classif_tab.eeg_fft_classif_tab import EegFftClassifTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
# from tabs.tab4.tab import Tab4
from tabs.mini_game_tab.mini_game_tab import MiniGameTab
from tabs.brain_3D_tab.brain_3D_tab import Brain3DTab
# Game
from game.main import RunGame


class OpenBciGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gv = GlobVar()  # Create the global variable that will be
                             # in many of this project classes
    
    def create_gui(self):
        self.setWindowTitle('OpenBCI GUI')
        self.setWindowIcon(QtGui.QIcon('./logo/polycortex_logo.png'))
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Running the experiment ...')

        self.main_window = MainWindow(self.gv)
        self.setCentralWidget(self.main_window)

        self.show()

    def create_menu_bar(self):
        main_menu = self.menuBar()
        self.controlPanel = QMenu('&System Control Panel')
        ## Action
        # OpenBCI
        self.create_openbci_menu()
        # Fake data
        self.create_stream_fake_data_menu()
        # From File
        self.create_stream_from_file_menu()
        # Connect the btn in the menubar to the print name function
        for btn in [self.openbci, self.fake_data, self.choose_file]:
            btn.triggered.connect(partial(self.choose_stream, btn))

        main_menu.addMenu(self.controlPanel)
        self.create_menu_start_game()
        main_menu.addMenu(self.menuGame)

    def choose_stream(self, btn):
        """Create a function that will print the name of the menubar
        btn that was selected"""
        self.gv.stream_origin[0] = btn.name

    def start_the_game(self):
        """Start the miniGame"""
        run_game = RunGame()
        run_game.start()

    def create_openbci_menu(self):
        self.openbci = QtGui.QAction(QIcon('./logo/openbci_logo.png'),
                                     'OpenBci')  # TODO: ALEXM Utiliser une liste déroulante plutot
        self.openbci.setShortcut('Ctrl+O')
        self.openbci.setStatusTip('Stream data from Openbci...')
        self.openbci.name = 'Stream from OpenBCI'
        self.controlPanel.addAction(self.openbci)

    def create_stream_fake_data_menu(self):
        self.fake_data = QtGui.QAction('Fake data')
        self.fake_data.setStatusTip(
            """Stream data from artificially generated data...""")
        self.fake_data.name = 'Stream from fake data'
        self.controlPanel.addAction(self.fake_data)

    def create_stream_from_file_menu(self):
        self.from_file = QMenu(title='From file')
        self.from_file.setStatusTip(
            """Stream data from previously saved file...""")
        self.controlPanel.addMenu(self.from_file)

        self.choose_file = QtGui.QAction('From file')
        self.choose_file.setStatusTip(
            """Choose the file from which you want to stream data...""")
        self.from_file.addAction(self.choose_file)
        self.choose_file.name = 'Stream from file'

    def create_menu_start_game(self):
        # ---Start game---
        self.menuGame = QMenu(title='&Start game')
        self.start_game = QtGui.QAction('Start game...')
        self.start_game.setStatusTip("""Press to start the mini game...""")
        self.start_game.triggered.connect(self.start_the_game)
        self.menuGame.addAction(self.start_game)


class MainWindow(QWidget):                                                     # TODO: ALEXM, Change the name of this class so that it fit the model of all the class that are include inside each other in the pyqt framework
    def __init__(self, gv):
        """
        """
        super().__init__()
        self.gv = gv
        self.init_font()
        self.init_win()

    def init_font(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(50)

    def init_win(self):
        """Create the layout ant add all the required tabs to it"""
        layout = QVBoxLayout(self)

        tabs_w_list = QTabWidget()

        tabs_name = ['EEG & FFT live graph', 'Experiments', 'EEG static graph',
                     'Mini Game', '3D brain']
        tabs_class = [EegFftClassifTab, ExperimentTab, StaticGraphTab,
                      MiniGameTab, Brain3DTab]
        tabs_w = []

        for i, tab_name in enumerate(tabs_name):
            tabs_w.append(QWidget())
            tabs_w_list.addTab(tabs_w[i], tab_name)
            if i <= 2:
                tabs_class[i](self, tabs_w[i], self.gv)
            else:
                tabs_class[i](self, tabs_w[i])

        # Add tabs to widget
        layout.addWidget(tabs_w_list)
        self.setLayout(layout)

