import numpy as np
from scipy.ndimage.interpolation import shift

def uniformize_data(emg_signal, len_signal):
    # Uniformize data
    emg_signal = emg_signal - np.average(emg_signal)
    avg = np.average(emg_signal)
    emg_signal = shift(emg_signal, len_signal / 2 - np.argmin(emg_signal),
                       cval=avg)
    min_sig = np.min(emg_signal)
    max_sig = np.max(emg_signal)
    emg_signal = emg_signal / (max_sig - min_sig)
    return emg_signal