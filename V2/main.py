import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import sys
# --My Packages--
from V2.GUI.main_window import MainWindow


def main():
    # win = pg.GraphicsWindow()
    app = QApplication(sys.argv)


    main_window = MainWindow()
    main_window.show()
    # sys.exit(app.exec_())
    QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    main()

