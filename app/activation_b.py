from PyQt5.QtWidgets import *
from functools import partial

def activation_b(layout, name, func_conn, pos, color, toggle=False):
    b = QPushButton(name)
    b.setStyleSheet('background-color: {}'.format(color))
    if toggle:
        b.setCheckable(True)
        b.toggled.connect(partial(func_conn))
    else:
        b.clicked.connect(partial(func_conn))
    layout.addWidget(b, *pos)
    
    
