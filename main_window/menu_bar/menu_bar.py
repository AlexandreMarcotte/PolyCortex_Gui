# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from .menu_action import MenuAction
from main_window.menu_bar.menu_file import MenuFile
from .menu_game import MenuGame


class MenuBar:
    def __init__(self, main_window, gv):
        self.main_window = main_window
        self.gv = gv

        self.main_menu = self.main_window.menuBar()

        self.controlPanel = QMenu('&System Control Panel')
        self.main_menu.addMenu(self.controlPanel)

        self.menu_game = MenuGame(self.gv, name='&Start game')
        self.main_menu.addMenu(self.menu_game)

        self.add_action_to_control_panel()

    def add_action_to_control_panel(self):
        ## Create menu action
        # OpenBCI
        self.openbci_actn = MenuAction(
                name='OpenBCI', gv=self.gv, icon_path='./img/openbci_logo.png',
                status_tip='Stream data from Openbci...', shortcut='Ctrl+O' )
        self.controlPanel.addAction(self.openbci_actn)
        # PCB
        self.pcb_actn = MenuAction(
                name="PolyCortex's PCB", gv=self.gv,
                icon_path='./img/polycortex_logo_alpha_background.png',
                status_tip='Stream the data from PolyCortex PCB' )
        self.controlPanel.addAction(self.pcb_actn)
        # Muse
        self.muse_actn = MenuAction(
                name='Muse', gv=self.gv, icon_path='./img/muse.png',
                status_tip='Stream data from Muse headband...' )
        self.controlPanel.addAction(self.muse_actn)
        # Fake data
        self.synthetic_data_actn = MenuAction(
                name='Synthetic data', gv=self.gv, icon_path='./img/sinus.png',
                status_tip='Stream data from artificially generated data...')
        self.controlPanel.addAction(self.synthetic_data_actn)
        # From File
        self.menu_file = MenuFile(
                name='File', gv=self.gv, main_window=self.main_window,
                status_tip='Stream data from previously saved file...')
        self.controlPanel.addMenu(self.menu_file)