from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from app.colors import *


class Label(QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""font-weight: 420; 
                            background-color: {label_grey}; 
                            font-size: 10pt;""")
        self.setMaximumHeight(26)
