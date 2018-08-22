# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
# # to show 3D data:
from nibabel import load
import pyqtgraph.opengl as gl

import numpy as np

class Tab4(object):
    def __init__(self, main_window, tab4):
        self.main_window = main_window
        self.tab4 = tab4

    def create_tab4(self):
        self.tab4.layout = QHBoxLayout(self.main_window)

        self.create_3D_brain_volume()

        self.tab4.setLayout(self.tab4.layout)

    def create_3D_brain_volume(self):
        # get MRI data
        nii = load('inplane001.nii')
        data = nii.get_data()
        # To complete for the lack of sampling in the third dimension
        data = np.repeat(data, repeats=4, axis=2)
        # Create viewer
        w = gl.GLViewWidget()
        w.setCameraPosition(0, 0, 90)
        w.opts['distance'] = 500
        self.tab4.layout.addWidget(w)
        # w.show()
        # create color image channels
        d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
        d2[..., 0] = data * (255. / (data.max() / 1))
        d2[..., 1] = d2[..., 0]
        d2[..., 2] = d2[..., 0]
        d2[..., 3] = d2[..., 0]
        d2[..., 3] = (d2[..., 3].astype(float) / 255.) ** 2 * 255

        # RGB orientation lines (optional)
        d2[:, 0, 0] = [255, 0, 0, 255]
        d2[0, :, 0] = [0, 255, 0, 255]
        d2[0, 0, :] = [0, 0, 255, 255]

        v = gl.GLVolumeItem(d2, sliceDensity=1, smooth=False)
        v.translate(-d2.shape[0] / 2, -d2.shape[1] / 2, -150)
        w.addItem(v)
