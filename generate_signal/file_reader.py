from collections import deque
import numpy as np


def read_data_from_file(file_name, N_CH=8):
    """Read data from CSV to create the static graph"""
    n_data = 0
    # Count the total number of data point
    with open(file_name, 'r') as f:
        for _ in f:
            n_data += 1

    print('n_data', n_data)
    # Create the data structure as a deque
    data = [deque(np.zeros(n_data), maxlen=n_data) for _ in range(N_CH)]
    t = deque(np.zeros(n_data), maxlen=n_data)
    exp = deque(np.zeros(n_data), maxlen=n_data)

    # Read all the lines in the file and add them to the data deque
    with open(file_name, 'r') as f:
        for all_ch_line in f:
            try:
                all_ch_line = all_ch_line.strip().split(',')                   # TODO: ALEXM read the file as a csv instead
                eeg_ch = all_ch_line[0:N_CH]
                t.append(float(all_ch_line[N_CH]))
                exp.append(float(all_ch_line[N_CH+1]))
                for ch_no, ch in enumerate(eeg_ch):
                    data[ch_no].append(float(ch))
            except IndexError as e:
                print('INDEX_ERROR: ', all_ch_line)

    return data, t, exp
