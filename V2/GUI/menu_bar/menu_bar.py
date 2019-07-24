from PyQt5.QtWidgets import *
from .control_panel_menu import ControlPanelMenu
from .menu_game import MenuGame


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.control_panel_menu = ControlPanelMenu(main_window)
        self.addMenu(self.control_panel_menu)

        self.menu_game = MenuGame(name='&Start game', main_window=main_window)
        self.addMenu(self.menu_game)




