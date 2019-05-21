from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *


class SettingCombobox(QComboBox):
    def __init__(self, layout, name, pos, param, editable=True, cols=1,
                 tip=None):
        super().__init__()

        self._name = name
        self._pos = pos
        self._param = param
        self._editable = editable
        self._cols = cols
        self._tip = tip

        self._shift = 0

        self.add_param_combobox_to_layout(layout)

    def set_txt_label_appearance(self):
        l = QLabel(self._name)
        l.setFrameShape(QFrame.Panel)
        l.setFrameShadow(QFrame.Sunken)
        l.setLineWidth(1)
        l.setAlignment(Qt.AlignCenter)
        l.setStyleSheet(
                f"""font-weight: 420; 
                background-color: {label_grey}; 
                font-size: 10pt;""")
        l.setMaximumHeight(26)
        return l

    def add_param_combobox_to_layout(self, layout):
        # Label
        self.add_label_to_layout(layout)
        # Combobox
        self.add_combobox_to_layout(layout)

    def add_label_to_layout(self, layout):
        if self._name is not None:
            l = self.set_txt_label_appearance()
            layout.addWidget(l, *self._pos)
            self._shift = 1

    def add_combobox_to_layout(self, layout):
        for val in self._param:
            self.addItem(val)
        self.setEditable(self._editable)
        if self._tip is not None:
            self.setToolTip(self._tip)
        self.setStyleSheet('font-size: 10pt;')
        layout.addWidget(
                self, self._pos[0] + self._shift, self._pos[1], 1, self._cols)

    def _connect(self, func):
        self.activated[str].connect(func)
