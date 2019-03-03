# --General Packages--
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from app.rotated_button import RotatedButton
from functools import partial
from PyQt5 import QtCore, QtGui
import sys
import os
# --My Packages--
from machine_learning.cnn_1D import Learner
from app.pyqt_frequently_used import select_file
from .stream_console import Stream_console


class MachineLearningTab(QWidget):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv

        self.learner = Learner()

        self.pg_layout = self.create_tab()
        self.tool_dock = self.create_settings_dock()

        self.create_open_settings_button()
        result_dock, self.training_plot = self.create_result_dock()
        self.create_test_unseen_data_dock(result_dock)

        self.lr = 0

    def create_tab(self):
        layout = QHBoxLayout(self)
        self.dock_area = DockArea()

        pg_layout = pg.LayoutWidget()
        layout.addWidget(pg_layout)
        layout.addWidget(self.dock_area)

        self.setLayout(layout)
        return pg_layout

    def create_open_settings_button(self):
        # open_settings_dock = Dock('open_settings_button', size=(1, 1))
        # open_settings_dock.hideTitleBar()
        # self.dock_area.addDock(open_settings_dock, 'left')
        # open_settings_layout = pg.LayoutWidget()
        # open_settings_dock.addWidget(open_settings_layout)
        # btn
        b = RotatedButton('Settings', orientation='east')
        b.setCheckable(True)
        b.setChecked(True)
        b.clicked.connect(self.open_toolbox)
        self.pg_layout.addWidget(b)
        # open_settings_layout.addWidget(b)

    def create_result_dock(self):
        # txt
        result_dock = Dock('Results')

        self.dock_area.addDock(result_dock, 'right')
        result_layout = pg.LayoutWidget()
        result_dock.addWidget(result_layout)
        # Form
        result_form = QGroupBox('')
        f_l = QFormLayout()
        choose_save_file_b = QPushButton('Save model path')
        choose_save_file_edit = QLineEdit('')
        choose_save_file_b.clicked.connect(
            partial(self.select_f, edit=choose_save_file_edit,
                    f_extension='.h5', open=True, type='save'))
        f_l.addRow(choose_save_file_b, choose_save_file_edit)
        result_form.setLayout(f_l)
        result_layout.addWidget(result_form, 0, 0, 1, 3)
        # Start training button
        start_training_b = QPushButton('Start training')
        start_training_b.setMaximumWidth(150)
        start_training_b.clicked.connect(self.train_learner_cnn)
        result_layout.addWidget(start_training_b, 0, 3)
        # txt
        self.result_txt_edit = QTextEdit()
        result_layout.addWidget(self.result_txt_edit, 1, 0)
        # Plot
        training_plot = pg.PlotWidget()
        training_plot.plotItem.setLabel(axis='left', units='epoc')
        training_plot.plotItem.setLabel(axis='bottom', units='accuracy')
        result_layout.addWidget(training_plot, 1, 1, 1, 3)
        return result_dock, training_plot

    @QtCore.pyqtSlot(str)
    def write_consol_message_in_txt_edit(self, message):
        # https://stackoverflow.com/questions/29799016/pyside-qtextedit-or-qplaintextedit-update-faster
        # I have to do an other thread so that the gui is still 'alive'
        # during the training You can see that the gui is dead during the
        #  training because you cannot click on any buttons every thing
        # is frozen
        self.result_txt_edit.moveCursor(QtGui.QTextCursor.End)
        self.result_txt_edit.insertPlainText(message)

    # Put on a new thread
    def train_learner_cnn(self, ):
        sys.stdout = Stream_console(self.result_txt_edit, self)
        sys.stdout.message.connect(self.write_consol_message_in_txt_edit)

        hist, model = self.learner.train_cnn()
        save_path = os.path.join(os.getcwd(), self.learner.save_model_path)
        model.save(self.learner.save_model_path)
        self.plot_results(self.training_plot, hist)
        # Put the stdout back to the console
        sys.stdout = sys.__stdout__

    def plot_results(self, plot, hist):
        # Legend
        plot.addLegend()
        # Accuracy
        plot.plot(hist.history['acc'], pen='g', name='result accuracy')
        # Validation
        plot.plot(hist.history['val_acc'], pen='b', name='results validation')

    def create_test_unseen_data_dock(self, result_dock):
        test_dock = Dock('Test unseen data')
        self.dock_area.addDock(test_dock, 'bottom', result_dock)
        test_layout = pg.LayoutWidget()
        # Form
        test_form = QGroupBox('')
        f_l = QFormLayout()
        # Select model
        select_model_b = QPushButton('Load model path')
        select_model_edit = QLineEdit('')
        select_model_b.clicked.connect(
            partial(self.select_f, edit=select_model_edit, f_extension='.h5',
                    open=True))
        f_l.addRow(select_model_b, select_model_edit)

        test_form.setLayout(f_l)
        test_layout.addWidget(test_form, 0, 0, 1, 2)
        # Start button
        start_test_b = QPushButton('Start testing')
        start_test_b.setMaximumWidth(150)
        test_layout.addWidget(start_test_b, 0, 2)
        # Plot
        unseen_data_plot = pg.PlotWidget()
        # unseen_data_plot.addItem()
        test_layout.addWidget(unseen_data_plot, 1, 0, 1, 3)
        unseen_data_curve = unseen_data_plot.plot()
        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setRange(0, 200)
        test_layout.addWidget(slider, 2, 0, 1, 3)
        # Connect start testing button
        start_test_b.clicked.connect(partial(
                self.test_learner_cnn_on_unseen_data, slider,
                unseen_data_curve, unseen_data_plot))

        test_dock.addWidget(test_layout)

    def select_f(self, edit, open=True, f_extension='.csv', type='save'):
        f_name = select_file(
                self.gv.main_window, open=open, f_extension=f_extension)
        edit.setText(f_name)
        if type == 'save':
            self.learner.save_model_path = f_name
        elif type == 'load':
            self.learner.load_model_path = f_name

    def plot_sig_and_prediction_class(
                self, predictions, curve, plot, sig_no):
        # plot.setTile(f'{sig_no} is so cool ')
        real = self.learner.y_val[sig_no].argmax()
        plot.getPlotItem().setTitle(
                f'''Prediction: {predictions[sig_no]} 
                  / Real: {real}''')
        if predictions[sig_no] == real:
            color = 'g'
        else:
            color = 'r'
        self.set_signal_to_plot(curve, sig_no, color)

    def set_signal_to_plot(self, curve, sig_no, color):
        sig = self.learner.x_val[sig_no]
        sig = sig.reshape(len(sig))
        curve.setPen(color)
        curve.setData(sig)

    def test_learner_cnn_on_unseen_data(
                self, slider, unseen_data_curve, unseen_data_plot):
        predictions, predictions_proportion = self.learner.predict()
        slider.valueChanged[int].connect(
                partial(self.plot_sig_and_prediction_class, predictions,
                    unseen_data_curve, unseen_data_plot))
        slider.setRange(0, len(self.learner.x_val)-1)
        self.set_signal_to_plot(unseen_data_curve, 0, 'b')

    def create_settings_dock(self):
        tool_dock = Dock('tool dock', size=(4, 1))
        tool_dock.hideTitleBar()
        self.dock_area.addDock(tool_dock, 'left')
        tool_layout = pg.LayoutWidget()
        tool_dock.addWidget(tool_layout)

        tb = QToolBox()

        self.create_training_toolbox(tb)
        self.create_optimizer_toolbox(tb)
        self.create_neural_network_layer_toolbox(tb)

        tool_layout.addWidget(tb, 0, 0)

        add_layer_b = QPushButton('+ Add a layer')
        tool_layout.addWidget(add_layer_b, 1, 0)

        return tool_dock

    def create_toolbox(self, tb, toolbox_name, form_dict):
        form_gr = QGroupBox('')
        f_l = QFormLayout()
        f_l = self.create_and_connect_spin_box(form_dict, f_l, toolbox_name)
        form_gr.setLayout(f_l)
        tb.addItem(form_gr, toolbox_name)

    def create_optimizer_toolbox(self, tb):
        optimizer_combo = self.init_combo_param(
                ['SGD', 'Adagrad', 'Adadelta', 'Adam', 'Nadam'])

        self.optimizer_form_dict = {
                'optimizer combo': optimizer_combo,
                'activation unit': self.init_combo_param(['relu']),
                'lr': pg.SpinBox(
                        value=self.learner.optimizer_params['lr'],
                        step=0.00001),
                'beta_1': pg.SpinBox(
                        value=self.learner.optimizer_params['beta_1'],
                        step=0.1),
                'beta_2': pg.SpinBox(
                        value=self.learner.optimizer_params['beta_2'],
                        step=0.0001),
                'epsilon': pg.SpinBox(
                        value=self.learner.optimizer_params['epsilon'],
                        step=1e-09),
                'decay': pg.SpinBox(
                        value=self.learner.optimizer_params['decay'],
                        step=0.1)
                }
        self.create_toolbox(tb, 'Optimizer', self.optimizer_form_dict)

    def create_neural_network_layer_toolbox(self, tb):
        self.nn_form_dict = {
                'n filter': pg.SpinBox(
                        value=self.learner.n_filters[0], step=1),
                'n pool': pg.SpinBox(value=self.learner.n_pool, step=1),
                'n conv': pg.SpinBox(value=self.learner.n_conv[0], step=1),
                'droupout rate':pg.SpinBox(
                        value=self.learner.dropout[0], step=0.05)
                }
        self.create_toolbox(tb, 'Layer #1', self.nn_form_dict)

    def create_training_toolbox(self, tb):
        self.model_form = {
                'n epoch': self.create_spin_box(
                        value=self.learner.n_epoch, step=1),
                'batch size': pg.SpinBox(value=self.learner.batch_size, step=1)
                }
        self.create_toolbox(tb, 'Training', self.model_form)

    def create_spin_box(self, value, step=1):
        spin_box = pg.SpinBox(value=value, step=step)
        spin_box.step = step
        return spin_box

    def init_combo_param(self, params):
        combo = QComboBox()
        for p in params:
            combo.addItem(p)
        return combo

    def create_and_connect_spin_box(self, form_dict, f_l, toolbox_name):
        for title_label, param in form_dict.items():
            if type(param) is pg.SpinBox:
                try:
                    print('param', param.step)
                except AttributeError as e:
                    param.step = 0.1
                    print('error', e)

                param.valueChanged.connect(partial(
                        self.change_var_value, title_label, toolbox_name,
                        param.step))
            elif type(param) is QComboBox:
                param.activated[str].connect(partial(
                        self.change_var_value, title_label, toolbox_name))
            f_l.addRow(QLabel(f'{title_label}: '), param)
        return f_l

    def change_var_value(self, var_name, toolbox_name, value, step=0.1):
        if type(step) is int:
            print('step')

        exec(f'self.learner.{var_name.replace(" ", "_")} = {value}')

    def open_toolbox(self, checked):
        if checked:
            self.tool_dock.show()
        else:
            self.tool_dock.hide()




# import threading
# stream_consol.message.connect(self.on_consol_stream_message)


# class TrainWorker(threading.Thread):
#     """Cannot use a thread on the training I really need to find a way
#     to use a buffer that is more similar to the one in the print statement
#     a buffer that show every line one after the other
#     Not sure it's posible..."""
#     def __init__(self, learner, machine_learning_tab):
#         super().__init__()
#         self.learner = learner
#         self.machine_learning_tab = machine_learning_tab
#
#     def run(self):
#         hist, model = self.learner.train_cnn()
#         self.machine_learning_tab.plot_results(
#                 self.machine_learning_tab.training_plot, hist)


# class WatchBufferValue(threading.Thread):
#     def __init__(self, stream_consol, result_txt_edit):
#         super().__init__()
#         self.stream_consol = stream_consol
#         self.result_txt_edit = result_txt_edit
#
#     def run(self):
#         while 1:
#             self.result_txt_edit.insertPlainText(self.stream_consol.x)






