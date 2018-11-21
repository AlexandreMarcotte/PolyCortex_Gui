from time import time, sleep
from random import random, randint
from math import pi
from numpy import sin
import numpy as np
import threading


class CreateFakeData(threading.Thread):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv
        # Variable necessary to generate fake signal
        ## time
        self.t = np.linspace(0, 2 * pi, self.gv.DEQUE_LEN)
        ## signal shape
        self.m = 1000
        self.s1 = self.m * sin(self.t)
        self.s2 = self.m * sin(20 * self.t)
        self.s3 = self.m * sin(40 * self.t)
        self.s4 = self.m * 5 * sin(60 * self.t)

        # 100 harmonic signal to test filtering
        self.s = []
        for freq in range(70, 100, 2):
            self.s.append(self.m * sin(freq * self.t))

    def add_signal_to_queue(self, signal, ch):
        self.gv.data_queue[ch].append(signal)
        self.gv.all_data[ch].append(signal)

    def run(self):
        """Create random data and a time stamp for each of them"""
        while 1:
            self.gv.n_data_created[0] += 1
            i = self.gv.n_data_created[0] % len(self.t)

            for ch in range(self.gv.N_CH):
                rnd_impulse = randint(0, 100)
                # Set impulse size to be added to the signal once every 100 data
                if rnd_impulse == 0:
                    imp = 5 * self.m
                else:
                    imp = 0
                if ch == 0:
                    signal = self.s1[i] + self.s3[i]+ self.s4[i] + random()*self.m + imp
                elif ch == 1:
                    signal = 20 * self.s1[i] + 5
                elif ch == 2:
                    signal = 10 * self.s2[i]
                elif ch == 3:
                    signal = self.s3[i]
                elif ch == 4:
                    signal = self.s4[i]
                elif ch == 5:
                    signal = 0
                    for s in self.s:
                        signal += s[i]
                else:
                    signal = random() * self.m

                self.add_signal_to_queue(signal, ch)

            # Add current time
            current_t = time() - self.gv.t_init
            self.gv.t_queue.append(current_t)
            self.gv.all_t.append(current_t)

            # Add experiment type values 
            if self.gv.experiment_type != 0:
                self.gv.experiment_queue.append(self.gv.experiment_type[0])
                self.gv.all_experiment_val.append(self.gv.experiment_type[0])
                self.gv.experiment_type = 0
            else:
                self.gv.experiment_queue.append(0)
                self.gv.all_experiment_val.append(0)

            sleep(0.0017)