# --General packages--
from PyQt5.QtWidgets import QApplication
import sys
# --My packages--
from app.dispatcher import Dispatcher
from main_window.mainwindow import MainWindow
from pyqtgraph.dockarea.Dock import DockLabel
from app.update_pyqtgraph_dock_tab import update_style_patched


def main():
    # pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
    # Start the multigraphes
    DockLabel.updateStyle = update_style_patched
    app = QApplication(sys.argv)

    N_CH = 8
    DEQUE_LEN = 1250
    gv = Dispatcher(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN)                            # Create the global variable that will be
                                                                               # in many of this project classes
    # Create the Gui
    openbci_gui = MainWindow(app, gv)
    gv.openbci_gui = openbci_gui

    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



