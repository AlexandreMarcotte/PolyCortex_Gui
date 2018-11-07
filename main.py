# General packages
from collections import deque
import numpy as np
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
# Dark theme
import qdarkstyle

import atexit

# My packages
from mainwindow_menubar import MainWindow


def main():
    # Start the multigraphes
    app = QApplication(sys.argv)
    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # Create the Gui
    openbci_gui = MainWindow()
    openbci_gui.create_mainwindow()

    @atexit.register   # work only if click on x on the window
    def save_data_at_exit():
        pass
        # open_bci_gui.main_window.tab_1.write_to_file()                         # TODO: ALEXM: kill all the thread here

    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



