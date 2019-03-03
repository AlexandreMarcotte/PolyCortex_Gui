# --General packages--
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
import atexit
# --My packages--
from app.dispatcher import Dispatcher
from mainwindow import MainWindow
from save.write_to_file import write_to_file
import pyqtgraph as pg


def main():
    # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
    pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
    # Start the multigraphes
    app = QApplication(sys.argv)

    N_CH = 8
    DEQUE_LEN = 1250
    gv = Dispatcher(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN)                            # Create the global variable that will be
                                                                               # in many of this project classes
    # Create the Gui
    openbci_gui = MainWindow(app, gv)
    gv.openbci_gui = openbci_gui

    @atexit.register   # work only if click on x on the window
    def save_data_at_exit():
        # pass
        print('saving')
        write_to_file(gv)                                                    # TODO: ALEXM: kill all the thread here (create a JOIN method in the threads)

    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



