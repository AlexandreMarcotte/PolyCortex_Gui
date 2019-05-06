import numpy as np


def put_data_into_array(data):
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
