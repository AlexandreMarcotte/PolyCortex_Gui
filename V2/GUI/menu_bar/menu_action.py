from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from functools import partial


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


