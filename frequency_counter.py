import time


class FrequencyCounter(object):
    def __init__(self, loop_name):
        self.initial_time = time.time()
        self.last_time_elapsed = 0
        self.loop_name = loop_name

    def print_freq(self, n_val_created):
        """ Plot the frequency of a loop once every second"""
        time_elapsed = int(time.time() - self.initial_time)
        if time_elapsed > self.last_time_elapsed:
            self.last_time_elapsed = time_elapsed
            # print('--------',
            #       'time_elapsed:', time_elapsed,
            #       'n_val_created:', n_val_created,
            #       'FREQUENCY: ', n_val_created / time_elapsed,
            #       'of {l_n}'.format(l_n=self.loop_name))
