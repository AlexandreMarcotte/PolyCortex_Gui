from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5, filter_type='bandpass'):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype=filter_type, analog=False)
    return b, a


def butter_bandpass_filter(
            data, lowcut, highcut, fs, order=5, filter_type='bandpass'):
    b, a = butter_bandpass(lowcut, highcut, fs, order, filter_type)
    y = lfilter(b, a, data)
    return y


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

