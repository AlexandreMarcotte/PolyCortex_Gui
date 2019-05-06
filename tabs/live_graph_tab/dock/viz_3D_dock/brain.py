# -- General Packages --
from random import randrange
from PyQt5 import QtCore
# -- My Packages --
from .put_nii_data_into_array import put_data_into_array
from .create_3D_scatter_plot_from_3D_np_array import create_3D_scatter_plot_from_np_array
from .create_3D_volume_from_3D_np_array import create_3D_volume_from_3D_np_array


class Brain:
    def __init__(
            self, brain_nii_data, type='scatter', show_box=False,
            show_axis=False):

        self.brain_3d_array = put_data_into_array(brain_nii_data)

        if type == 'scatter':
            self.item = create_3D_scatter_plot_from_np_array(
                    self.brain_3d_array)

        if type == 'volume':
            self.item = create_3D_volume_from_3D_np_array(
                    self.brain_3d_array, scale=3, show_box=show_box,
                    show_axis=show_axis)

