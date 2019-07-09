from PyQt5.QtCore import QFile, QTextStream
from V2.utils.BreezeStyleSheets import breeze_resources
import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class DarkModeAction(QAction):
    def __init__(self, tool_bar, main_window):
        self.main_window = main_window

        base_path = os.getcwd()
        path = os.path.join(base_path, 'GUI/img/light_mode.png')
        super().__init__(QIcon(path), 'change light style', tool_bar)

        self.setStatusTip('Change style to qdarkstyle')
        self.triggered.connect(self.change_light_style)

    def change_light_style(self):
        file = QFile(":/dark.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.main_window.app.setStyleSheet(stream.readAll())
