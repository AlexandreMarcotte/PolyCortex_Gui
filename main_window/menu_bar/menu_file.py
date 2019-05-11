# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from main_window.menu_bar.menu_action import MenuAction


class MenuFile(QMenu):
    def __init__(self, name, gv, main_window, status_tip):
        super().__init__()

        self.name = name
        self.gv = gv
        self.main_window = main_window
        self.setTitle(f'Choose {name}')

        self.setStatusTip(status_tip)
        self.add_action()

    def add_action(self):
        self.actn = MenuAction(
                name='File', gv=self.gv, main_window=self.main_window,
                icon_path='./img/file.png',
                status_tip='Choose the file from which you want to stream data...')
        self.addAction(self.actn)

