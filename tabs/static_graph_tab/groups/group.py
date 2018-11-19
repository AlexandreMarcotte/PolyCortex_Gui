# -- General Packages --
from PyQt5.QtWidgets import *


class Group:
    def create_gr_and_layout(self, name, parent_layout=None, ch=None):
        layout = QGridLayout()
        layout.setContentsMargins(0, 3, 0, 0)
        gr = QGroupBox(name)
        gr.setLayout(layout)
        if parent_layout is not None:
            parent_layout.addWidget(gr, ch, 0)
        return layout, gr
