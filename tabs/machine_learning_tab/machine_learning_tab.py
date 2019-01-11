from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from PyQt5 import QtCore
from app.rotated_button import RotatedButton


class MachineLearningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_tab()
        self.tool_dock = self.create_tool_dock()
        result_dock = self.create_result_dock()
        self.create_test_unseen_data_dock(result_dock)

    def create_tab(self):
        layout = QHBoxLayout(self)
        self.dock_area = DockArea()
        layout.addWidget(self.dock_area)
        # btn
        self.setLayout(layout)

    def create_result_dock(self):
        # txt
        result_dock = Dock('Results')
        self.dock_area.addDock(result_dock, 'right')
        result_layout = pg.LayoutWidget()
        # Form
        result_form = QGroupBox('')
        f_l = QFormLayout()
        f_l.addRow(QPushButton('Choose save file'), QLineEdit(
                '/home/alex/Desktop/openBCI_eeg_gui/tabs/live_graph_tab/dock'))

        result_form.setLayout(f_l)
        result_layout.addWidget(result_form, 0, 0, 1, 2)

        result_dock.addWidget(result_layout)
        # Plot
        unseen_data_plot = pg.PlotWidget()
        result_layout.addWidget(unseen_data_plot, 1, 1)
        # txt
        result_layout.addWidget(QTextEdit(), 1, 0)
        return result_dock

    def create_test_unseen_data_dock(self, result_dock):
        test_dock = Dock('Test unseen data')
        self.dock_area.addDock(test_dock, 'bottom', result_dock)
        test_layout = pg.LayoutWidget()
        # Form
        test_form = QGroupBox('')
        f_l = QFormLayout()
        f_l.addRow(QPushButton('Select model'), QLineEdit(''))
        f_l.addRow(QPushButton('Select data'), QLineEdit(''))
        test_form.setLayout(f_l)
        test_layout.addWidget(test_form, 0, 0)
        # Plot
        unseen_data_plot = pg.PlotWidget()
        test_layout.addWidget(unseen_data_plot, 1, 0)

        test_dock.addWidget(test_layout)

    def create_tool_dock(self):
        tool_dock = Dock('tool dock')
        tool_dock.hideTitleBar()
        self.dock_area.addDock(tool_dock, 'left')
        tool_layout = pg.LayoutWidget()
        tool_dock.addWidget(tool_layout)

        tb = QToolBox()

        self.create_model_toolbox(tb)
        self.create_optimizer_toolbox(tb)
        self.create_neural_network_layer_toolbox(tb)

        tool_layout.addWidget(tb, 0, 0)

        add_layer_b = QPushButton('+ Add a layer')
        tool_layout.addWidget(add_layer_b, 1, 0)


        return tool_dock

    def create_optimizer_toolbox(self, tb):
        optimizer_form = QGroupBox('')
        f_l = QFormLayout()

        optimizer_combo = QComboBox()
        params = ['SGD', 'Adagrad', 'Adadelta', 'Adam', 'Nadam']
        for p in params:
           optimizer_combo.addItem(p)
        f_l.addRow(QLabel('optimizer type: '), optimizer_combo)
        f_l.addRow(QLabel('lr: '), pg.SpinBox(value=0.0001, step=0.00001))
        f_l.addRow(QLabel('beta_1: '), pg.SpinBox(value=0.9, step=0.1))
        f_l.addRow(QLabel('beta_2: '), pg.SpinBox(value=0.999, step=0.0001))
        f_l.addRow(QLabel('epsilon: '), pg.SpinBox(value=1e-08, step=1e-09))
        f_l.addRow(QLabel('decay: '), pg.SpinBox(value=0.0, step=0.1))
        optimizer_form.setLayout(f_l)

        tb.addItem(optimizer_form, 'Optimizer')

    def create_neural_network_layer_toolbox(self, tb):
        layer_form = QGroupBox('')
        f_l = QFormLayout()

        f_l.addRow(QLabel('n filter: '), pg.SpinBox(value=20, step=1))
        f_l.addRow(QLabel('n pool: '), pg.SpinBox(value=10, step=1))
        f_l.addRow(QLabel('n conv: '), pg.SpinBox(value=12, step=1))

        layer_form.setLayout(f_l)
        tb.addItem(layer_form, 'Layer #1')

    def create_model_toolbox(self, tb):
        layer_form = QGroupBox('')
        f_l = QFormLayout()

        activation_combo = QComboBox()
        params = ['relu']
        for p in params:
            activation_combo.addItem(p)
        f_l.addRow(QLabel('optimizer type: '), activation_combo)
        f_l.addRow(QLabel('Dropout rate: '), pg.SpinBox(value=0.5, step=0.1))

        layer_form.setLayout(f_l)
        tb.addItem(layer_form, 'Model')

    def open_tool_box(self, checked):
        if checked:
            print('open tool box')
            self.tool_dock.show()
        else:
            self.tool_dock.hide()


