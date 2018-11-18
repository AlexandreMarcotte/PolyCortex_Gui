# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
# # to show 3D data:
from nibabel import load
import pyqtgraph.opengl as gl

import numpy as np
import os

class Brain3DTab:
    def __init__(self, main_window, tab_w):
        self.main_window = main_window
        self.tab_w = tab_w
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.tab_w.layout = QHBoxLayout(self.main_window)

        self.create_3D_brain_volume()

        self.tab_w.setLayout(self.tab_w.layout)

    def create_3D_brain_volume(self):
        # get MRI data
        nii_path = 'tabs/brain_3D_tab/inplane001.nii'
        nii = load(os.path.join(os.getcwd(), nii_path))
        data = nii.get_data()
        # To complete for the lack of sampling in the third dimension
        data = np.repeat(data, repeats=4, axis=2)

        # Create viewer
        w = gl.GLViewWidget()
        w.setCameraPosition(0, 0, 90)
        w.opts['distance'] = 500
        self.tab_w.layout.addWidget(w)
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
