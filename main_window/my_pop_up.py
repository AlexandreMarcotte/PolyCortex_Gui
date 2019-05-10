from PyQt5.QtWidgets import *


class MyPopUp(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Learn more about PolyCortex')

        self.layout = QVBoxLayout()
        self.info = QLabel(
            'PolyCortex is Polytechnique Montreal club for\n'
            'neuroscience and BCI, it was founded in 2013 \n'
            'by Benjamin De Leener & Gabriel Mangeat\n\n'
            'To learn more about PolyCortex visite the link: \n\n\n'
            'http://polycortex.polymtl.ca/')
        self.layout.addWidget(self.info)
        self.setLayout(self.layout)
