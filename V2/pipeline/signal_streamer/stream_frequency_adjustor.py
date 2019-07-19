from time import time


class StreamFrequencyAdjustor:
    def __init__(self, current_t_stamp=time(), desired_stream_period=100):
        self.first_pass = True
        self.current_t_stamp = current_t_stamp
        self.desired_stream_period = desired_stream_period
        self.time_for_one_cycle = desired_stream_period
        self.adjust_value = desired_stream_period / 10

    def adjust_real_stream_period(self, current_t_stamp, real_stream_period):
        """Count the time between cycle of data production by the streamer
            if this time is higher than the sleep time of the cycle
            (real_stream_period) will be decrease """
        if self.first_pass:
            self.get_time_stamp_on_first_pass()
        else:
            self.time_for_one_cycle = current_t_stamp - self.current_t_stamp
            self.current_t_stamp = current_t_stamp
            # self._show_info(self.time_for_one_cycle)
        return self._adjust_real_stream_period(real_stream_period)

    def get_time_stamp_on_first_pass(self):
            self.current_t_stamp = time()
            self.first_pass = False

    def _show_info(self, time_for_one_cycle):
        print('-----------------------------------------------')
        print('time_for_one_cycle: ', time_for_one_cycle,
              ' vs ', self.desired_stream_period)

    def _adjust_real_stream_period(self, real_stream_period):
        adjust_value = abs(self.time_for_one_cycle - self.desired_stream_period) / 5
        if self.time_for_one_cycle > self.desired_stream_period:
            real_stream_period -= adjust_value
        else:
            real_stream_period += adjust_value
        # Make sure the value is not negative
        if real_stream_period < 0:
            real_stream_period = 0

        return real_stream_period
