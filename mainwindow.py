# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
import qdarkstyle
# from pyqtgraph.Qt import Rect
import os
from functools import partial
# --My packages--
from tabs.tab_widget import TabWidget
from game.main import RunGame
from app.pyqt_frequently_used import select_file


class MainWindow(QMainWindow):
    def __init__(self, app, gv):
        super().__init__()
        self.app = app
        self.gv = gv
        self.name = 'PolyCortex Gui'
        self.openbci_logo_path = './img/openbci_logo.png'
        self.file_icon_path = './img/file.png'
        self.polycortex_logo_path = './img/polycortex_logo.png'
        self.sinus_logo_path = './img/sinus.png'
        self.icon = QtGui.QIcon(self.polycortex_logo_path)
        self.pos = (0, 0)
        self.size = (1350, 950)
        self.intro_message = 'Running the experiment ...'

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

        self.tab_w = TabWidget(self, self.gv)
        self.setCentralWidget(self.tab_w)

        self.show()

    def create_menu_bar(self):
        self.main_menu = self.menuBar()
        self.controlPanel = QMenu('&System Control Panel')
        ## Create menu action
        # OpenBCI
        self.create_openbci_menu()
        # PCB
        self.create_pcb_menu()
        # Muse
        self.create_muse_menu()
        # Fake data
        self.create_stream_fake_data_menu()
        # From File
        self.create_stream_from_file_menu()
        # Connect the btn in the menubar to the choose stream function
        for btn in [self.openbci, self.pcb, self.fake_data, self.choose_file,
                    self.muse]:
            btn.triggered.connect(partial(self.choose_stream, btn))

        self.main_menu.addMenu(self.controlPanel)
        self.create_menu_start_game()
        self.main_menu.addMenu(self.menuGame)


    def create_openbci_menu(self):
        self.openbci = QtGui.QAction(
                QIcon(self.openbci_logo_path), 'OpenBci')                    # TODO: ALEXM Utiliser une liste déroulante plutot
        self.openbci.setShortcut('Ctrl+O')
        self.openbci.setStatusTip('Stream data from Openbci...')
        self.openbci.name = 'Stream from OpenBCI'
        self.controlPanel.addAction(self.openbci)

    def create_pcb_menu(self):
        self.pcb = QtGui.QAction(
                QIcon(self.polycortex_logo_path), "PolyCortex's PCB")
        self.pcb.setStatusTip('Stream the data from PolyCortex PCB')
        self.pcb.name = 'Stream from pcb'
        self.controlPanel.addAction(self.pcb)

    def create_stream_fake_data_menu(self):
        self.fake_data = QtGui.QAction(QIcon(self.sinus_logo_path), 'Synthetic data')
        self.fake_data.setStatusTip(
                'Stream data from artificially generated data...')
        self.fake_data.name = 'Stream from synthetic data'
        self.controlPanel.addAction(self.fake_data)

    def create_stream_from_file_menu(self):
        self.from_file = QMenu(title='From file')
        self.from_file.setStatusTip(
                'Stream data from previously saved file...')
        self.controlPanel.addMenu(self.from_file)

        self.choose_file = QtGui.QAction(
                QIcon(self.file_icon_path), 'Choose file...')
        self.choose_file.setStatusTip(
                'Choose the file from which you want to stream data...')
        self.from_file.addAction(self.choose_file)
        self.choose_file.name = 'Stream from file'

    def create_muse_menu(self):
        self.muse = QtGui.QAction(
                QIcon('./img/muse.png'), 'Muse')                               # TODO: ALEXM Utiliser une liste déroulante plutot
        self.muse.setStatusTip('Stream data from Muse headband...')
        self.muse.name = 'Stream from Muse'
        self.controlPanel.addAction(self.muse)

    def choose_stream(self, btn):
        """Create a function that will print the name of the menubar
        btn that was selected"""
        self.gv.stream_origin = btn.name
        print(btn.name, 'is the stream location...')

        if btn.name == 'Stream from file':
            self.choose_streaming_file()

    def choose_streaming_file(self):
        f_name = select_file(self, open=True)
        if f_name:
            self.gv.stream_path = f_name
            print('Streaming from: ', f_name)

    def create_menu_start_game(self):
        # ---Start game---
        self.menuGame = QMenu(title='&Start game')
        self.start_game = QtGui.QAction('Start platformer game...')
        self.start_game.setStatusTip('Press to start the mini game...')
        self.start_game.triggered.connect(self.start_the_game)
        self.menuGame.addAction(self.start_game)

    def start_the_game(self):
        """Start the miniGame"""
        run_game = RunGame(self.gv)
        run_game.start()

    def create_toolbar(self):
        main_tb = QToolBar('main actions')
        main_tb.addAction(self.create_exit_action())
        main_tb.addAction(self.create_dark_mode_activator())
        main_tb.addAction(self.create_polycortex_info_btn())
        self.addToolBar(main_tb)
        # tree_tb = QToolBar('tree toolbar')
        # tree_tb.setOrientation(Qt.Vertical)
        #
        # tree_action = QAction('1:Tree', self)
        # tree_tb.addAction(tree_action)
        # a2 = QAction('2:', self)
        # tree_tb.addAction(a2)
        # self.addToolBar(Qt.LeftToolBarArea, tree_tb)

    def create_exit_action(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'app/exit.png')
        exitIcon = QIcon(path)
        exit_actn = QAction(exitIcon, 'Exit', self)
        exit_actn.setShortcut('Ctrl+Q')
        exit_actn.setStatusTip('Exit application')
        exit_actn.triggered.connect(self.close)
        return exit_actn

    def create_dark_mode_activator(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'img/light_mode.png')
        light_act = QAction(QIcon(path), 'change light style', self)
        light_act.setStatusTip('Change style to qdarkstyle')
        light_act.triggered.connect(self.change_light_style)
        return light_act

    def create_polycortex_info_btn(self):
        polycortex_icon = QIcon(self.polycortex_logo_path)
        polyCortex_actn = QAction(polycortex_icon, 'PolyCortex', self)
        polyCortex_actn.setStatusTip('Get information about PolyCortex Society')
        polyCortex_actn.triggered.connect(self.show_polycortex_info_page)
        self.w = None
        return polyCortex_actn

    def show_polycortex_info_page(self):
        print('show polycortex infor page')
        self.polycortex_info_win = MyPopup()
        self.polycortex_info_win.setGeometry(QRect(100, 200, 400, 200))
        self.polycortex_info_win.show()

    def change_light_style(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Learn more about PolyCortex')

        self.layout = QVBoxLayout()
        self.info = QLabel(
               'PolyCortex is Polytechnique Montreal club for\n'
               'neuroscience and BCI, it was founded in 2013 \n'
               'by Benjamin De Leener & Gabriel Mangeat\n\n'
               'To learn more about PolyCortex visite the link: \n\n\n'
               'http://polycortex.polymtl.ca/')
        self.layout.addWidget(self.info)
        self.setLayout(self.layout)

