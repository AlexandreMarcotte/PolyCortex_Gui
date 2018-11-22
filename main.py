# --General packages--
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
# Dark theme
import atexit
# --My packages--
from app.dispatcher import Dispatcher, VizProcess, FilterProcess
from mainwindow import MainWindow
from save.write_to_file import write_to_file


def main():
    # Start the multigraphes
    app = QApplication(sys.argv)

    N_CH = 8
    DEQUE_LEN = 1250
    viz_process = VizProcess(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN)
    filter_process = FilterProcess(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN)
    gv = Dispatcher(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN,
                    process=[viz_process, filter_process])                     # Create the global variable that will be
                                                                               # in many of this project classes
    # Apply dark theme
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())                    # With this I cannot add lines to the windows (ex there is no lines arround group box)
    # Create the Gui
    openbci_gui = MainWindow(app, gv)

    @atexit.register   # work only if click on x on the window
    def save_data_at_exit():
        print('saving')
        # write_to_file(gv)                                      # TODO: ALEXM: kill all the thread here (create a JOIN method in the threads)

    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



