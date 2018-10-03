# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

# from pyqtgraph.Qt import QtGui
import os
import numpy as np
from time import time

# My packages
from init_variables import InitVariables
from frequency_counter import FrequencyCounter
# -- Tabs --
from tabs.tab1 import Tab1
from tabs.tab2 import Tab2
from tabs.tab3 import Tab3
from tabs.tab4 import Tab4
from tabs.tab5 import Tab5
from tabs.tab6 import Tab6


class OpenBciGui(QMainWindow):
    def __init__(self):
        super().__init__()
    
    def create_gui(self):
        self.setWindowTitle('OpenBCI GUI')
        self.setWindowIcon(QtGui.QIcon('./logo/polycortex_logo.png'))
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Running the experiment ...')

        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

        self.show()

    def create_menu_bar(self):
        main_menu = self.menuBar()
        # ---File---
        self.menuFile = QMenu(title='&System Control Panel')
        # # Action
        self.openbci = QtGui.QAction('OpenBci')                                # TODO: ALEXM Utiliser une liste déroulante plutot
        self.openbci.setShortcut('Ctrl+O')
        self.openbci.setStatusTip('Stream data from Openbci...')
        self.fake_data = QtGui.QAction('Fake data')
        self.fake_data.setStatusTip("""Stream data from artificially 
                                       generated data...""")
        self.from_file = QtGui.QAction('From file')
        self.from_file.setStatusTip("""Stream data from previously  
                                       saved file...""")
        # self.quit_action.triggered.connect(....)
        self.menuFile.addAction(self.openbci)
        self.menuFile.addAction(self.fake_data)
        self.menuFile.addAction(self.from_file)

        main_menu.addMenu(self.menuFile)
        # ---Start game---
        self.menuEdit = QMenu(title='&Start game')
        main_menu.addMenu(self.menuEdit)


class MainWindow(QWidget, InitVariables):
    def __init__(self):
        """
        """
        super().__init__()

        self.init_font()

        self.init_win()

    def init_font(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(50)

    def init_win(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()


        # Add tabs
        self.tabs.addTab(self.tab1, 'EEG & FFT live graph')
        self.tabs.addTab(self.tab2, 'Experiments')
        self.tabs.addTab(self.tab3, 'EEG static graph')
        # self.tabs.addTab(self.tab4, 'Classification certitude')
        self.tabs.addTab(self.tab5, 'Mini Game')
        self.tabs.addTab(self.tab6, '3D representation')

        # Compose tabs
        # - Tab 1
        self.tab_1 = Tab1(self, self.tab1, self.experiment_type, 
                          self.experiment_queue)
        self.tab_1.create_tab1()
        # - Tab 2
        self.tab_2 = Tab2(self, self.tab2, self.experiment_type,
                          self.experiment_queue)
        self.tab_2.create_tab2()
        # - Tab 3
        self.tab_3 = Tab3(self, self.tab3)
        self.tab_3.create_tab3()

        # - Tab 4
        # self.tab_4 = Tab4(self, self.tab4)
        # self.tab_4.create_tab()

        # - Tab 5
        self.tab_5 = Tab5(self, self.tab5)
        self.tab_5.create_tab5()
        
        # - Tab 6
        self.tab_6 = Tab6(self, self.tab6)
        self.tab_6.create_tab6()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

