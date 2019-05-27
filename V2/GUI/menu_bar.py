from PyQt5.QtWidgets import *


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.file_menu = FileMenu()
        self.addMenu(self.file_menu)


class FileMenu(QMenu):
    def __init__(self):
        super().__init__('File')
        self.new_action = MenuAction('new')
        self.addAction(self.new_action)


class MenuAction(QAction):
    pass
