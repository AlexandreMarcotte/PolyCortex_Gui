# -- General packages
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from functools import partial
# -- My packages --
from app.colors import *


class FileGroup:
    def __init__(self, main_win, static_graph_file_name, create_stationnary_plot):
        self.main_win = main_win
        self.static_graph_file_name = static_graph_file_name
        self.create_stationnary_plot = create_stationnary_plot

        self.data_path = None
        self.open_file_layout, self.open_file_group = self.create_open_file()
        self.create_open_data_from_file_layout(self.open_file_layout)

    def create_open_file(self):
        open_file_layout = QGridLayout()
        open_file_group = QGroupBox('Open file')
        open_file_group.setLayout(open_file_layout)
        return open_file_layout, open_file_group

    def create_open_data_from_file_layout(self, open_file_layout):
        self.add_choose_file_btn(open_file_layout)
        self.add_data_path_line(open_file_layout)
        self.add_open_file_b(open_file_layout)

    def add_choose_file_btn(self, open_file_layout):
        chose_file_b = QtGui.QPushButton('Choose file containing data')
        chose_file_b.setStyleSheet(f'background-color: {blue_b}')
        chose_file_b.clicked.connect(partial(self.open_static_data_file))
        open_file_layout.addWidget(chose_file_b, 0, 0)

    def add_data_path_line(self, open_file_layout):
        """Create text box to show or enter path to data file"""
        self.data_path = QtGui.QLineEdit(self.static_graph_file_name)
        open_file_layout.addWidget(self.data_path, 0, 1)

    def add_open_file_b(self, open_file_layout):
        open_file_b = QtGui.QPushButton('Open File')
        open_file_b.clicked.connect(partial(self.create_stationnary_plot))
        open_file_layout.addWidget(open_file_b, 0, 2)

    @pyqtSlot()
    def open_static_data_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_win, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.data_path.setText(file_name)
            self.static_graph_file_name = file_name
