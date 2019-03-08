# -- General packages--
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from functools import partial
import pyqtgraph as pg
import numpy as np
# -- My packages --
from app.colors import *
from generate_signal.file_reader import read_data_from_file
from ... static_graph_tab.groups.group import Group


class FileSelector(Group):
    def __init__(self, name, win, gv, right_gr, left_gr):
        super().__init__()
        self.name = name
        self.win = win
        self.gv = gv
        self.right_gr = right_gr
        self.left_gr = left_gr
        # Initialize data lists before reading                                 TODO: ALEXM: create a panda dataframe instead
        self.data = []
        self.t = []
        self.exp = []
        self.file_name = './experiment_csv/pinch_close.csv'

        self.gr, self.path_line_edit = self.init_layout()

    def init_layout(self):
        layout, gr = self.create_gr_and_layout(self.name)
        self.add_choose_file_b(layout)
        path_line_edit = self.add_data_path_line_edit(layout)
        self.add_open_file_b(layout)
        self.pbar = self.add_progress_bar(layout)
        return gr, path_line_edit

    def add_choose_file_b(self, layout):
        b = QtGui.QPushButton('Choose file containing data')
        b.setStyleSheet(f'''background-color: {dark_blue_tab};
                        color: {white}; ''')
        b.clicked.connect(partial(self.choose_file))
        layout.addWidget(b, 0, 0)

    def add_data_path_line_edit(self, layout):
        """Create text box to show or enter path to data file"""
        path_line_edit = QtGui.QLineEdit(self.file_name)
        layout.addWidget(path_line_edit, 0, 1)
        return path_line_edit

    def add_open_file_b(self, layout):
        open_file_b = QtGui.QPushButton('Open File')
        open_file_b.clicked.connect(partial(self.read_data, layout))
        layout.addWidget(open_file_b, 0, 2)

    def add_progress_bar(self, layout):
        pbar = QProgressBar()
        layout.addWidget(pbar, 0, 3)
        pbar.setValue(0)
        return pbar

    @pyqtSlot()
    def choose_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getOpenFileName(
            self.win, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if f_name:
            self.path_line_edit.setText(f_name)
            self.f_name = f_name

    @pyqtSlot()
    def read_data(self, layout):
        data, t, exp = \
            read_data_from_file(self.path_line_edit.text(), N_CH=self.gv.N_CH)   # clean this part
        for ch in range(self.gv.N_CH):
            fg = self.right_gr.full_graphs[ch]
            slider = self.right_gr.sliders[ch]
            acg = self.left_gr.avg_classif_graphs[ch]
            pgs = self.left_gr.portion_graphs[ch]
            cg = self.left_gr.classif_graphs[ch]

            self.pbar.setValue(int(100 * (ch+1)/self.gv.N_CH))
            # Right panel
            fg.plot_data(data[ch], color='w')
            slider.setMaximum(len(data[0]))
            # Left panel
            pgs.data = np.array(data[ch])
            pgs.t = np.array(t)
            pgs.plot_data(data[ch], color='g')
            pgs.add_all_experimentation_regions(ch, exp)
            classified_data = self.left_gr.classif_graphs[ch].classify_data(data[ch])
            cg.plot_data(classified_data, color='b')

            acg.curve = acg.plot_data(
                np.zeros(self.gv.emg_signal_len), color='b')
            acg.classif_region_curve = acg.plot_data(
                np.zeros(self.gv.emg_signal_len), color='r')
            acg.combo_box_curve = acg.plot_data(
                np.zeros(self.gv.emg_signal_len), color='y')
            acg.classified_data = classified_data
            acg.update_pos_and_avg_graph(classif_region_pos=0)
