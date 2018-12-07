from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


def create_gr(margin=False):
    gr = QGroupBox()
    l = QGridLayout()
    if not margin:
        l.setContentsMargins(0, 0, 0, 0)
    gr.setLayout(l)
    return gr, l

def create_splitter(first_gr, second_gr):
    s = QSplitter(Qt.Horizontal)
    s.addWidget(first_gr)
    s.addWidget(second_gr)
    return s

def create_txt_label(name):
    l = QLabel(name)
    l.setFrameShape(QFrame.Panel)
    l.setFrameShadow(QFrame.Sunken)
    l.setLineWidth(1)
    l.setAlignment(Qt.AlignCenter)
    l.setStyleSheet(f'font-weight: 440;')
    return l

def create_param_combobox(
        layout, name, pos, param, conn_func, editable=True,
        cols=1):
    l = create_txt_label(name)
    layout.addWidget(l, *pos)
    combo_box = QComboBox()
    for val in param:
        combo_box.addItem(val)
    combo_box.setEditable(editable)
    combo_box.activated[str].connect(conn_func)
    layout.addWidget(combo_box, pos[0]+1, pos[1], 1, cols)

def add_triplet_txt_box(line, layout):
    for i in range(3):
        pos_t = QtGui.QLineEdit(str(0))
        layout.addWidget(pos_t, line, i)

