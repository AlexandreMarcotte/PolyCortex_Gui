# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon
# from pyqtgraph.Qt import QtGui
import os
from functools import partial
# My packages
from app.global_variables import GlobVar

# from tabs.tab_widget import TabWidget
from tabs.eeg_fft_classif_tab.eeg_fft_classif_tab import EegFftClassifTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
from tabs.mini_game_tab.mini_game_tab import MiniGameTab
from tabs.brain_3D_tab.brain_3D_tab import Brain3DTab
## Game
from game.main import RunGame


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gv = GlobVar()  # Create the global variable that will be
                             # in many of this project classes
        self.name = 'Openbci Gui'
        self.icon = QtGui.QIcon('./img/polycortex_logo.png')
        self.pos = (0, 0)
        self.size = (1350, 950)
        self.intro_message = 'Running the experiment ...'

        self.tabs = {EegFftClassifTab(self.gv): 'EEG & FFT live graph',
                     ExperimentTab(self.gv): 'Experiments',
                     StaticGraphTab(self.gv): 'EEG static graph',
                     MiniGameTab(): 'Mini Game',
                     Brain3DTab(): '3D brain'}

        self.init_mainwindow()
    
    def init_mainwindow(self):
        self.setWindowTitle(self.name)
        self.setWindowIcon(self.icon)
        self.setGeometry(*self.pos, *self.size)
        # Add a menu bar
        self.create_menu_bar()
        # Add a toolbar
        self.create_toolbar()
        # message at the bottom
        self.statusBar().showMessage(self.intro_message)

        self.create_tabs()

    def create_tabs(self):
        tab_w = QTabWidget()

        for name, tab in self.tabs.items():
            tab_w.addTab(name, tab)

        self.setCentralWidget(tab_w)

        self.show()

    def create_menu_bar(self):
        main_menu = self.menuBar()
        self.controlPanel = QMenu('&System Control Panel')
        ## Create menu action
        # OpenBCI
        self.create_openbci_menu()
        # Muse
        self.create_muse_menu()
        # Fake data
        self.create_stream_fake_data_menu()
        # From File
        self.create_stream_from_file_menu()
        # Connect the btn in the menubar to the choose stream function
        for btn in [self.openbci, self.fake_data, self.choose_file, self.muse]:
            btn.triggered.connect(partial(self.choose_stream, btn))

        main_menu.addMenu(self.controlPanel)
        self.create_menu_start_game()
        main_menu.addMenu(self.menuGame)

    def create_openbci_menu(self):
        self.openbci = QtGui.QAction(QIcon('./img/openbci_logo.png'),
                                     'OpenBci')                                # TODO: ALEXM Utiliser une liste déroulante plutot
        self.openbci.setShortcut('Ctrl+O')
        self.openbci.setStatusTip('Stream data from Openbci...')
        self.openbci.name = 'Stream from OpenBCI'
        self.controlPanel.addAction(self.openbci)

    def create_stream_fake_data_menu(self):
        self.fake_data = QtGui.QAction('Fake data')
        self.fake_data.setStatusTip(
            'Stream data from artificially generated data...')
        self.fake_data.name = 'Stream from fake data'
        self.controlPanel.addAction(self.fake_data)

    def create_stream_from_file_menu(self):
        self.from_file = QMenu(title='From file')
        self.from_file.setStatusTip(
            'Stream data from previously saved file...')
        self.controlPanel.addMenu(self.from_file)

        self.choose_file = QtGui.QAction('Choose file...')
        self.choose_file.setStatusTip(
            'Choose the file from which you want to stream data...')
        self.from_file.addAction(self.choose_file)
        self.choose_file.name = 'Stream from file'

    def create_muse_menu(self):
        self.muse = QtGui.QAction(QIcon('./img/muse.png'),
                                     'Muse')                                   # TODO: ALEXM Utiliser une liste déroulante plutot
        self.muse.setStatusTip('Stream data from Muse headband...')
        self.muse.name = 'Stream from Muse'
        self.controlPanel.addAction(self.muse)

    def choose_stream(self, btn):
        """Create a function that will print the name of the menubar
        btn that was selected"""
        self.gv.stream_origin[0] = btn.name
        print(btn.name)

        if btn.name == 'Stream from file':
            self.choose_streaming_file()

    def choose_streaming_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.stream_path = file_name

    def create_menu_start_game(self):
        # ---Start game---
        self.menuGame = QMenu(title='&Start game')
        self.start_game = QtGui.QAction('Start game...')
        self.start_game.setStatusTip('Press to start the mini game...')
        self.start_game.triggered.connect(self.start_the_game)
        self.menuGame.addAction(self.start_game)

    def start_the_game(self):
        """Start the miniGame"""
        run_game = RunGame()
        run_game.start()

    def create_toolbar(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'app/exit.png')
        exitAct = QAction(QIcon(path), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)