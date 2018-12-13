from time import sleep
import threading


# The following code is from the fake data streamer : TODO: ALEXM: Modification of this code to be able to stream from muse headset
class StreamFromMuse(threading.Thread):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv
        # port = '/dev/ttyUSB0'  # if using Linux
        # self.board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
        # self.board.enable_filters()
        # print("Board Instantiated")
        # sleep(1)  # TODO: I changed it to 1 and it was 5 before see if there is a problem
    #
    # def run(self):
    #     self.board.start_streaming(self.gv.collect_data)

