from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from functools import partial
from app.pyqt_frequently_used import select_file


class MenuAction(QtGui.QAction):
    def __init__(self, name, gv, main_window=None, icon_path=None,
                 status_tip='', shortcut=None):
        super().__init__()

        self.name = name
        self.gv = gv
        self.main_window = main_window

        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconText(f'From {name}')

        if shortcut:
            self.setShortcut(shortcut)

        self.setStatusTip(status_tip)

        self.connect_to_select_stream()

    def connect_to_select_stream(self):
        self.triggered.connect(partial(self.set_selected_stream, self))

    def set_selected_stream(self, menu_action):
        """Set the name of the button that was selected in the gv class"""
        self.gv.stream_origin = menu_action.name

        if menu_action.name == 'File':
            self.set_stream_path()

    def set_stream_path(self):
        f_name = select_file(self.main_window, open=True)
        if f_name:
            self.gv.stream_path = f_name

