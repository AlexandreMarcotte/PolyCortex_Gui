from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band', analog=False)
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
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


# TODO: ALEXM: I tried to calculate the coeff a and b only one time at the beginning of the
# class, but it created even more oscillation in the signal (pourtant il semblait
# que les coefficients /taient toujours de meme valeur, je ne sais donc pas trop
# pourquoi ce comportement different se produit
# Tenter de revenir a cette conformation du code (mais en faisant en sorte que
# le filtrage commence uniquement apres qu'un certain nombre de données soit présent
# dans le deque (parce qu'il semble que le point problématique du filtre soit
# le tout début ou les nouvelles valeurs entre, une oscillation majeur se produit
