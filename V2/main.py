from pyqtgraph.Qt import QtGui
from PyQt5.QtWidgets import *
import sys
# --My Packages--
from V2.GUI.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    # app.setStyle('cleanlooks')
    main_window = MainWindow()
    main_window.show()
    QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    main()

