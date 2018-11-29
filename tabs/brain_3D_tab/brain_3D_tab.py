# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
# # to show 3D data:
from nibabel import load
import pyqtgraph.opengl as gl
import pyqtgraph as pg

import numpy as np
import os
from random import randrange

class Brain3DTab(QWidget):
    def __init__(self):
        super().__init__()
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.layout = QHBoxLayout(self)
        self.create_numpy_brain()

    def create_scatter_brain(self):
        obj_3d_creator = Obj3DCreator()

    def create_numpy_brain(self):
        obj_3d_creator = Obj3DCreator()
        brain_volume = obj_3d_creator.create_3D_brain_volume(show_axis=True)
        self.add_volume_to_view(brain_volume)

        self.setLayout(self.layout)

    def add_volume_to_view(self, v):
        # Create viewer
        w = gl.GLViewWidget()
        w.setCameraPosition(0, 0, 90)
        w.opts['distance'] = 500
        self.layout.addWidget(w)
        w.addItem(v)


class Obj3DCreator:
    def __init__(self):
        self.i = 0
        data = self.read_data()
        self.brain = self.put_data_into_array(data)

    def read_data(self):
        # get MRI data
        nii_path = '/home/alex/Desktop/openBCI_eeg_gui/tabs/brain_3D_tab/inplane001.nii'
        nii = load(os.path.join(os.getcwd(), nii_path))
        data = nii.get_data()
        return data

    def put_data_into_array(self, data):
        # To complete for the lack of sampling in the third dimension
        data = np.repeat(data, repeats=4, axis=2)
        # create color image channels
        brain = np.empty(data.shape + (4,), dtype=np.ubyte)
        brain[..., 0] = data * (255. / (data.max() / 1))
        brain[..., 1] = brain[..., 0]
        brain[..., 2] = brain[..., 0]
        brain[..., 3] = brain[..., 0]
        brain[..., 3] = (brain[..., 3].astype(float) / 255.) ** 2 * 255
        return brain

    def create_3D_scatter_plot(self, scale=1):
        pos = []
        color = []
        sx, sy, sz, _= self.brain.shape                                          # TODO: optimize this loop with numpy
        i = 0
        for x in range(sx):
            for y in range(sy):
                for z in range(sz):
                    if self.brain[x][y][z][3]>12:
                        # print(self.brain[x][y][z])
                        color.append(self.brain[x][y][z])
                        pos.append(np.array((x,y,z)))
        print('ok')

        item = gl.GLScatterPlotItem(pos=np.array(pos), color=(0,0.3,1,0.5),
                                         size=1, pxMode=True)
        item.translate(-self.brain.shape[0]/2 * scale,
                    -self.brain.shape[1]/2 * scale,
                    -self.brain.shape[2]/2 * scale)
        # item = pg.ScatterPlotItem(size=100, pen=pg.mkPen('w'))
        # spots = [{'pos': pos, 'size': 10} for pos in self.pos]
        # item.addPoints(spots)
        return item

    def create_3D_brain_volume(
            self, show_axis=False, show_box=False, scale=1):
        if show_axis:
            # RGB orientation lines (optional)
            self.brain[:, 1, 1] = [255, 0, 0, 255]  # R-x
            self.brain[1, :, 1] = [0, 255, 0, 255]  # G-y
            self.brain[1, 1, :] = [0, 0, 255, 255]  # B-z
        # Create a box at the extremity of the array
        if show_box:
            for i in (0, -1):
                self.brain[:, :, i] = [0, 255, 0, 20]
                self.brain[:, i, :] = [0, 255, 0, 20]
                self.brain[i, :, :] = [0, 255, 0, 20]

        v = gl.GLVolumeItem(self.brain, sliceDensity=1, smooth=False)
        v.translate(-self.brain.shape[0]/2 * scale,
                    -self.brain.shape[1]/2 * scale,
                    -self.brain.shape[2]/2 * scale)
        v.scale(scale, scale, scale)
        # v.translate(20 * brain.shape[0], 0, 0)

        self.shape_x = self.brain.shape[0]
        self.shape_y = self.brain.shape[1]
        self.shape_z = self.brain.shape[2]
        print(self.shape_x, self.shape_y, self.shape_z)

        return v






