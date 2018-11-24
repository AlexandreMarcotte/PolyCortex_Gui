from time import time


class FrequencyCounter:
    def __init__(self, gv):
        self.gv = gv
        self.last_n_data_collected = 0
        self.last_t = time()
        self.calcul_last_freq()
        self.t_between_calcul_freq = 0.3

    def update(self):
        # Calcul frequency less often
        self.calcul_last_freq()
        if self.freq < self.gv.desired_read_freq:
            self.adjust_freq_up()
            # print('UP')
        if self.freq > self.gv.desired_read_freq:
            self.adjust_freq_down()
            # print('     DOWN')
        # print(f'The sampling frequency in the last second is: \n {self.freq}')
        self.last_t = time()
        self.last_n_data_collected = self.gv.n_data_created

    def calcul_last_freq(self):
        delta_data = self.gv.n_data_created - self.last_n_data_collected
        delta_t = time() - self.last_t
        self.freq = delta_data / delta_t

    def adjust_freq_up(self):
        'Increase frequency: '
        self.gv.used_read_freq += 10                                          # TODO: use a variable increase so that it gets faster to the right frequency when this one is real far
        self.gv.read_period = 1 / self.gv.used_read_freq
        # print('Increase used_freq: ', self.gv.used_read_freq)

    def adjust_freq_down(self):
        self.gv.used_read_freq -= 10
        self.gv.read_period = 1 / self.gv.used_read_freq
        # print('Decrease used freq: ', self.gv.used_read_freq)

