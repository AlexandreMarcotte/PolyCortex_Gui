from PyQt5.QtWidgets import *
from .control_panel_menu import ControlPanelMenu


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.control_panel_menu = ControlPanelMenu(main_window)
        self.addMenu(self.control_panel_menu)

        # self.menu_game = MenuGame(self.gv, name='&Start game')
        # self.main_menu.addMenu(self.menu_game)




