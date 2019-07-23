from .menu_action import MenuAction
from PyQt5.QtWidgets import QMenu


class MenuFile(QMenu):
    def __init__(self, name, main_window=None, icon_path=None,
                 status_tip='', shortcut=None):
        super().__init__()

        self.main_window = main_window
        self.setTitle(f'Choose File')
        self.setStatusTip(status_tip)
        self.add_action(icon_path)

    def add_action(self, icon_path):
        self._choose_file_action = MenuAction(
            name='File', main_window=self.main_window, icon_path=icon_path,
            status_tip='Choose the file from which you want to stream data...')
        self.addAction(self._choose_file_action)
