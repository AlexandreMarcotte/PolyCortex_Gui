# -- General Packages --
from functools import partial
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from game.main import RunGame
# -- My Packages --
from app.pyqt_frequently_used import select_file


class MenuBar:
    def __init__(self, main_window, gv):
        self.main_window = main_window
        self.gv = gv

        self.openbci_logo_path = './img/openbci_logo.png'
        self.polycortex_logo_path_alpha_background = \
            './img/polycortex_logo_alpha_background.png'
        self.sinus_logo_path = './img/sinus.png'
        self.file_icon_path = './img/file.png'

        self.create_menu_bar()

    def create_menu_bar(self):
        self.main_menu = self.main_window.menuBar()
        self.controlPanel = QMenu('&System Control Panel')
        ## Create menu action
        # OpenBCI
        self.openbci_actn = self.create_openbci_actn()
        self.controlPanel.addAction(self.openbci_actn)
        # PCB
        self.create_pcb_menu()
        # Muse
        self.create_muse_menu()
        # Fake data
        self.fake_data = self.create_stream_fake_data_menu()
        self.controlPanel.addAction(self.fake_data)
        # From File
        self.create_stream_from_file_menu()
        # Connect the btn in the menubar to the choose stream function
        for btn in [self.openbci_actn, self.pcb, self.fake_data, self.choose_file,
                    self.muse]:
            btn.triggered.connect(partial(self.choose_stream, btn))

        self.main_menu.addMenu(self.controlPanel)
        self.create_menu_start_game()
        self.main_menu.addMenu(self.menuGame)


    def create_openbci_actn(self):
        openbci_actn = QtGui.QAction(
                QIcon(self.openbci_logo_path), 'OpenBci')                    # TODO: ALEXM Utiliser une liste déroulante plutot
        openbci_actn.setShortcut('Ctrl+O')
        openbci_actn.setStatusTip('Stream data from Openbci...')
        openbci_actn.name = 'Stream from OpenBCI'
        return openbci_actn

    def create_pcb_menu(self):
        self.pcb = QtGui.QAction(
            QIcon(self.polycortex_logo_path_alpha_background), "PolyCortex's PCB")
        self.pcb.setStatusTip('Stream the data from PolyCortex PCB')
        self.pcb.name = 'Stream from pcb'
        self.controlPanel.addAction(self.pcb)

    def create_stream_fake_data_menu(self):
        fake_data = QtGui.QAction(QIcon(self.sinus_logo_path), 'Synthetic data')
        fake_data.setStatusTip(
            'Stream data from artificially generated data...')
        fake_data.name = 'Stream from synthetic data'
        return fake_data

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
        f_name = select_file(self.main_window, open=True)
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
