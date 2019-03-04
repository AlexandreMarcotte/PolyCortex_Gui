class Wave:
    def __init__(self, freq_range):
        self.freq_range = freq_range

    def get_half_pos(self):
        return self.freq_range[0] + (self.get_delta_range()) / 2

    def get_delta_range(self):
        return self.freq_range[1] - self.freq_range[0]