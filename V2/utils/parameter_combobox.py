from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *


class ParameterCombobox(QComboBox):
    def __init__(self, layout, name, pos, param, editable=True,
            cols=1, tip=None):
        """ Create a parameter combobox under a text label """
        super().__init__()

        self.txt_label = self._create_txt_label(name)
        self._create_combobox(param, editable, tip)

        self._add_to_layout(layout, pos, cols)

    def _create_combobox(self, param, editable, tip):
        for val in param:
            self.addItem(val)
        self.setEditable(editable)
        if tip is not None:
            self.setToolTip(tip)
        self.setStyleSheet('font-size: 10pt;')

    def connect_cb(self, conn_func):
        self.conn_func = conn_func
        self.activated[str].connect(self.conn_func)

    def _add_to_layout(self, layout, pos, cols):
        layout.addWidget(self.txt_label, *pos)
        shift = 1
        layout.addWidget(self, pos[0] + shift, pos[1], 1, cols)

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
