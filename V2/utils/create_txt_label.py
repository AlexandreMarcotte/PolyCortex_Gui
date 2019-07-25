from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from V2.utils.colors import Color


class Label(QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""font-weight: 420; 
                            background-color: {Color.label_grey}; 
                            font-size: 10pt;""")
        self.setMaximumHeight(26)
