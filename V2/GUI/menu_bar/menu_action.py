from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from functools import partial
from app.pyqt_frequently_used import select_file


class MenuAction(QtGui.QAction):

    model = None

    def __init__(self, name, main_window=None, icon_path=None,
                 status_tip='', shortcut=None):
        super().__init__(name)

        self.name = name
        self.main_window = main_window

        self._set_status_tip(status_tip)
        self._set_shortcut(shortcut)
        self._set_icon(icon_path)
        self.connect_to_select_stream()

    def _set_status_tip(self, status_tip):
        self.setStatusTip(status_tip)

    def _set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)

    def _set_icon(self, icon_path):
        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconText(f'From {self.name}')

    def connect_to_select_stream(self):
        self.triggered.connect(
            partial(self.model.pipeline.update_streamer, self.name))

        # self.triggered.connect(partial(self.set_selected_stream, self))

    # def print_shit(self, menu_action):
    #     print('shittttt', menu_action.name)
    #     print('name of the class',  self.NAME_CLS)

    # def set_selected_stream(self, menu_action):
    #     """Set the name of the button that was selected in the gv class"""
    #     self.gv.stream_origin = menu_action.name
    #
    #     if menu_action.name == 'File':
    #         self.set_stream_path()
    #
    # def set_stream_path(self):
    #     f_name = select_file(self.main_window, open=True)
    #     if f_name:
    #         self.gv.stream_path = f_name
