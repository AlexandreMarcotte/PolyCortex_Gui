from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
import matplotlib.pyplot as plt
import numpy as np


def select_file(main_window, open=True, f_extension='.py'):
    """Set open to False if you want to get the file for saving"""
    # From: https://pythonspot.com/pyqt5-file-dialog/
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    # f_name, _ = QFileDialog.getFile
    if open:
        f_name, _ = QFileDialog.getOpenFileName(
            main_window, 'QFileDialog.getOpenFileName()', '',
            f'All Files (*);;Python Files (*{f_extension})', options=options)
    else:
        f_name, _ = QFileDialog.getSaveFileName(
            main_window, 'QFileDialog.getSaveFileName()', '',
            f'All Files (*);;Text Files (*{f_extension})', options=options)
    return f_name


def create_gr(margin=False):
    l = QGridLayout()
    if not margin:
        l.setContentsMargins(0, 0, 0, 0)
    gr = QGroupBox(f'')
    gr.setLayout(l)
    return gr, l


def create_splitter(first_gr, second_gr, direction=Qt.Horizontal):
    s = QSplitter(direction)
    s.addWidget(first_gr)
    s.addWidget(second_gr)
    return s


def create_txt_label(name):
    l = QLabel(name)
    l.setFrameShape(QFrame.Panel)
    l.setFrameShadow(QFrame.Sunken)
    l.setLineWidth(1)
    l.setAlignment(Qt.AlignCenter)
    l.setStyleSheet(f"""font-weight: 420; 
                        background-color: {label_grey}; 
                        font-size: 10pt;""")
    l.setMaximumHeight(26)
    return l


def create_param_combobox(
            layout, name, pos, param, conn_func=None, editable=True,
            cols=1, tip=None):
    # Label
    shift = 0
    if name is not None:
        l = create_txt_label(name)
        layout.addWidget(l, *pos)
        shift = 1
    # Combobox
    cb = QComboBox()
    for val in param:
        cb.addItem(val)
    cb.setEditable(editable)
    if conn_func is not None:
        cb.activated[str].connect(conn_func)
    if tip is not None:
        cb.setToolTip(tip)
    cb.setStyleSheet('font-size: 10pt;')
    layout.addWidget(cb, pos[0] + shift, pos[1], 1, cols)


class ClickableLineEdit(QLineEdit):
    def __init__(self, gv, i, name):
        super().__init__()
        self.gv = gv
        self.i = i
        self.name = name

        self.planes = ['x', 'y', 'z']
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        if self.name == 'position':
            self.gv.plane_to_move = self.planes[self.i]
        if self.name == 'angle':
            self.gv.rotation_axis = self.planes[self.i]
            print('angle', self.i)
        QLineEdit.mousePressEvent(self, event)


class TripletBox:
    def __init__(self, gv, name, col, layout, colors=None):
        self.gv = gv
        self.name = name

        self.N_COMBO_BOX = 3
        self.all_l_e = []
        self.add_triplet_txt_box(col, layout, colors)

    def add_triplet_txt_box(self, col, layout, colors=None):
        for i in range(self.N_COMBO_BOX):
            l_e = ClickableLineEdit(self.gv, i, self.name)
            if colors is not None:
                l_e.setStyleSheet(
                        f"""border-style: solid; 
                            border-color: {colors[i]}; 
                            border-width: 1px 1px 1px 1px;
                         """)
            l_e.setMaximumWidth(30)
            layout.addWidget(l_e, 1, col+i)
            self.all_l_e.append(l_e)


def create_cmap(z):
    cmap = plt.get_cmap('jet')
    min_z = np.min(z)
    max_z = np.max(z)
    cmap = cmap((z - min_z)/(max_z - min_z))
    return cmap

