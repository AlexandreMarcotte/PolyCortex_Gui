# Robotic arm from
# https://www.trossenrobotics.com/reactorx-200-robot-arm.aspx

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from pyqtgraph.dockarea import *
import numpy as np
import os


class ObjReader:
    def __init__(self, file_path):
        self.file_path = file_path

        self.faces = []
        self.verts = []
        self.faces_normals = []
        self.normal_indices = []

        self.read_file()
        # put in numpy arrays
        self.faces = np.array(self.faces)
        self.verts = np.array(self.verts, dtype=float)

        mesh_data = self.create_mesh_data()
        self.mesh_item = self.create_mesh_item(mesh_data)

    def read_file(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                line.strip()
                line = line.split(' ')
                data_type = line[0]
                if data_type == 'v':
                    self.extract_verts_from_obj_line(line)
                elif data_type == 'f':
                    self.extract_faces_from_obj_line(line)
                elif data_type == 'vn':
                    self.extract_faces_normals_from_obj_line(line)

    def extract_faces_from_obj_line(self, line):
        face = []
        for face_vals in line[1:]:
            face_vals = face_vals.split('//')
            face.append(int(face_vals[0]) - 1)
        self.normal_indices.append(int(face_vals[1]) - 1)
        self.faces.append(np.array(face))

    def extract_verts_from_obj_line(self, line):
        data = [float(_) for _ in line[1:]]
        self.verts.append(np.array(data))

    def extract_faces_normals_from_obj_line(self, line):
        data = [float(_) for _ in line[1:]]
        self.faces_normals.append(np.array(data))

    def create_mesh_data(self):
        return gl.MeshData(vertexes=self.verts, faces=self.faces)

    def create_mesh_item(self, mesh_item):
        return gl.GLMeshItem(
                meshdata=mesh_item, color=(0, 10, 210, 200), shader='shaded')


def add_obj_to_view(path, view, pos=None):
    obj = ObjReader(path)
    if pos:
        obj.mesh_item.translate(*pos)
    view.addItem(obj.mesh_item)


class RoboticArmDock:
    def __init__(self, tab_w, dock_bellow):
        super().__init__()
        self.tab_w = tab_w

        self.dock = Dock('Robotic Arm')
        self.tab_w.area.addDock(self.dock, 'above', dock_bellow)

        self.view = self.init_view()
        self.add_obj_to_view()
        self.view.show()

    def init_view(self):
        v = gl.GLViewWidget()
        self.dock.addWidget(v)
        v.setWindowTitle('')
        v.setCameraPosition(distance=1500, azimuth=-30, elevation=50)
        return v

    def add_obj_to_view(self):
        base_path = 'tabs/game_3D_tab/robotic_arm/arm_obj/'
        robot_arm_obj_files = ['base_fc.obj', 'shoulder_fc.obj', 'arm_fc.obj',
                               'forearm_fc.obj', 'wrist_fc.obj', 'hand_fc.obj',
                               'finger1_fc.obj', 'finger2_fc.obj']
        for obj_file in robot_arm_obj_files:
            add_obj_to_view(os.path.join(base_path, obj_file), self.view)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    view = gl.GLViewWidget()
    view.setCameraPosition(distance=320, azimuth=-90)
    view.show()
    add_obj_to_view('./arm_obj/base_fc.obj', view)
    QtGui.QApplication.instance().exec_()
