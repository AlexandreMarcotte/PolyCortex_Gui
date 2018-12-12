from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


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
            cols=1):
    l = create_txt_label(name)
    layout.addWidget(l, *pos)
    combo_box = QComboBox()
    for val in param:
        combo_box.addItem(val)
    combo_box.setEditable(editable)
    if conn_func is not None:
        combo_box.activated[str].connect(conn_func)
    layout.addWidget(combo_box, pos[0]+1, pos[1], 1, cols)


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
        QLineEdit.mousePressEvent(self, event)


class TripletBox:
    def __init__(self, gv, name, col, layout, colors=None):
        self.gv = gv
        self.name = name
        self.all_l_e = []
        self.add_triplet_txt_box(col, layout, colors)

    def add_triplet_txt_box(self, col, layout, colors=None):
        for i in range(3):
            l_e = ClickableLineEdit(self.gv, i, self.name)
            # l_e.textChanged[str].connect(partial(self.do_something, i))
            if colors is not None:
                l_e.setStyleSheet(
                        f"""border-style: solid; 
                            border-color: {colors[i]}; 
                            border-width: 1px 1px 1px 1px;
                         """)
            l_e.setMaximumWidth(30)
            layout.addWidget(l_e, 1, col+i)
            self.all_l_e.append(l_e)

