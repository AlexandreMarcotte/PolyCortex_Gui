import matplotlib.pyplot as plt
import numpy as np


def create_cmap(z):
    cmap = plt.get_cmap('jet')
    min_z = np.min(z)
    max_z = np.max(z)
    cmap = cmap((z - min_z)/(max_z - min_z))
    return cmap
