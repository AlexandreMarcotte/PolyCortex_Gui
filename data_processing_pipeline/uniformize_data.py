import numpy as np
from scipy.ndimage.interpolation import shift

def uniformize_data(s, len_signal):
    """Uniformize signal (s) """
    s = s - np.average(s)
    # avg = np.average(s)
    # s = s - avg
    # s = shift(s, len_signal / 2 - np.argmin(s), cval=avg)
    # min_sig = np.min(s)
    # max_sig = np.max(s)
    # s = s / (max_sig - min_sig)
    return s