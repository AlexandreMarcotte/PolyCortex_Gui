# When the file is named main I cannot import pygame
# For any other names it work
from pyqtgraph.Qt import QtGui
from PyQt5.QtWidgets import *
import sys
# --My Packages--
from V2.GUI.main_window import MainWindow


def main():
    main_window = MainWindow()
    main_window.show()
    main_window.excec()


if __name__ == '__main__':
    main()
