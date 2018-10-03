# General packages
from collections import deque
import numpy as np
# My packages
from visualisation_with_pyqt import OpenBciGui
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
# Dark theme
import qdarkstyle

import atexit
# Game
from game.main import RunGame


def main():
    # Game
    # run_game = RunGame()
    # run_game.start()

    # Start the multigraphes
    app = QApplication(sys.argv)
    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # Create the Gui
    open_bci_gui = OpenBciGui()
    open_bci_gui.create_gui()

    @atexit.register   # work only if click on x on the window
    def save_data_at_exit():
        open_bci_gui.main_window.tab_1.write_to_file()

    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



