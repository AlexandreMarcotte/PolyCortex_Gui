# -- General Packages --
from PyQt5.QtWidgets import *
from functools import partial
# -- My Packages --
from V2.utils.btn import Btn
from V2.utils.select_file import select_file


class FileSelectorDock:
    def __init__(self, external_layout):
        super().__init__()

        self._external_layout = external_layout

        self._init_choose_file_btn()
        self._init_line_edit()
        self._init_open_file_btn()
        external_layout.addWidget(QProgressBar(), 0, 3)

    def _init_choose_file_btn(self):
        self._choose_file_btn = Btn('Choose file containing data')
        self._external_layout.addWidget(self._choose_file_btn, 0, 0)
        self._choose_file_btn.clicked.connect(partial(self._select_file))

    def _init_open_file_btn(self):
        self.open_file_btn = Btn('Open File')
        self._external_layout.addWidget(self.open_file_btn, 0, 2)

    def _init_line_edit(self):
        self._line_edit = QLineEdit('/savepath.csv')
        self._external_layout.addWidget(self._line_edit, 0, 1)

    def _select_file(self):
        self._file_name = select_file()
        self._line_edit.setText(self._file_name)


