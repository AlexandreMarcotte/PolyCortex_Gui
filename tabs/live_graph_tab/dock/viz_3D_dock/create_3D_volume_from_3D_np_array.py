import pyqtgraph.opengl as gl


def create_3D_volume_from_3D_np_array(
        np_array_3D, show_axis=False, show_box=False, scale=1):

    if show_axis:
        # RGB orientation lines (optional)
        np_array_3D[:, 1, 1] = [255, 0, 0, 255]  # R-x
        np_array_3D[1, :, 1] = [0, 255, 0, 255]  # G-y
        np_array_3D[1, 1, :] = [0, 0, 255, 255]  # B-z

    # Create a box at the extremity of the array
    if show_box:
        for i in (0, -1):
            np_array_3D[:, :, i] = [0, 255, 0, 20]
            np_array_3D[:, i, :] = [0, 255, 0, 20]
            np_array_3D[i, :, :] = [0, 255, 0, 20]

    v = gl.GLVolumeItem(np_array_3D, sliceDensity=5, smooth=True)
    # Translate
    v.translate(-np_array_3D.shape[0]/2 * scale,
                -np_array_3D.shape[1]/2 * scale,
                -np_array_3D.shape[2]/2 * scale)
    # Scale
    v.scale(scale, scale, scale)
    # shape_x = np_array_3D.shape[0]
    # shape_y = np_array_3D.shape[1]
    # shape_z = np_array_3D.shape[2]

    return v

