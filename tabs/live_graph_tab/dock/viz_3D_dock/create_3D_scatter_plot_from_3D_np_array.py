import numpy as np
import pyqtgraph.opengl as gl


def create_3D_scatter_plot_from_np_array(np_array, scale=1):
    pos = []
    color = []
    sx, sy, sz, _ = np_array.shape                                              # TODO: optimize this loop with numpy
    i = 0
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                if np_array[x][y][z][3]>12:
                    # print(self.brain[x][y][z])
                    color.append(np_array[x][y][z])
                    pos.append(np.array((x,y,z)))

    item = gl.GLScatterPlotItem(
            pos=np.array(pos), color=(0,0.3,1,0.2), size=1, pxMode=True)
    item.translate(-np_array.shape[0]/2 * scale,
                   -np_array.shape[1]/2 * scale,
                   -np_array.shape[2]/2 * scale)

    # item = pg.ScatterPlotItem(size=100, pen=pg.mkPen('w'))
    # spots = [{'pos': pos, 'size': 10} for pos in self.pos]
    # item.addPoints(spots)
    return item
