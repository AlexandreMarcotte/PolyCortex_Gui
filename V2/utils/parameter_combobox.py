from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *


class ParameterCombobox:
    def __init__(self, layout, name, pos, param, conn_func=None, editable=True,
            cols=1, tip=None):
        """ Create a parameter combobox under a text label """

        self.txt_label = self._create_txt_label(name)
        self.cb = self.create_cb(param, editable, conn_func, tip)

        self._add_to_layout(layout, pos, cols)

    def create_cb(self, param, editable, conn_func, tip):
        cb = QComboBox()
        for val in param:
            cb.addItem(val)
        cb.setEditable(editable)
        # if conn_func is not None:
        #     cb.activated[str].connect(conn_func)
        if tip is not None:
            cb.setToolTip(tip)
        cb.setStyleSheet('font-size: 10pt;')
        return cb

    def connect_cb(self, conn_func):
        self.conn_func = conn_func
        self.cb.activated[str].connect(self.conn_func)

    def _add_to_layout(self, layout, pos, cols):
        layout.addWidget(self.txt_label, *pos)
        shift = 1
        layout.addWidget(self.cb, pos[0] + shift, pos[1], 1, cols)

    def _create_txt_label(self, name):
        if name is not None:
            label = QLabel(name)
            label.setFrameShape(QFrame.Panel)
            label.setFrameShadow(QFrame.Sunken)
            label.setLineWidth(1)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"""font-weight: 420; 
                                background-color: {label_grey}; 
                                font-size: 10pt;""")
            label.setMaximumHeight(26)
        return label

