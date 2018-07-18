# # -*- coding: utf-8 -*-
#
# # PLOTING the EEG data
# # Graph the data
# from PyQt5 import QtGui, QtCore
# from pyqtgraph.Qt import QtGui
# import numpy as np
# import pyqtgraph as pg
# from collections import deque
# import threading
# from numpy.fft import fft, fftfreq
# # My packages
# from frequency_counter import FrequencyCounter
# import sched, time
#
#
# # class UpdateMultipleChPlot(object):
# #     def __init__(self, plot, curve, data):
# #         self.plot = plot
# #         self.curve = curve
# #         self.data = data
# #
# #     def update_eeg(self, one_ch_deque, ch, num_itt):
# #         if num_itt % 50 == 0:
# #             self.plot[ch].setLabel('right', '{mean_ampl:.2f} muVrms'.format(
# #                                               mean_ampl=np.mean(one_ch_deque)))    # TODO: verifier l'unité
# #         self.curve[ch].setData(one_ch_deque)
#
#
# class EEG_graph(object):
#     def __init__(self, data_queue, win, layout, timer):
#         # Create 8 scrolling plot on the left of the window
#         # To display all the channels
#         self.win = win
#         self.data_queue = data_queue
#         self.layout = layout
#         self.timer = timer
#
#         self.N_DATA = len(data_queue[0])
#         self.N_SIGNALS = len(data_queue)
#         self.p = [[]] * self.N_SIGNALS
#         self.data = [None] * self.N_SIGNALS
#         self.curve = [None] * self.N_SIGNALS
#         self.update_func = []
#         self.num_itt = 0
#         self.DISPLAY_RATE = 1
#         self.frequency_counter = FrequencyCounter('EEG_frequency')
#
#         # Create the EEG channels
#         self.create_eeg_channels()
#
#     def create_eeg_channels(self):
#         self.win.setWindowTitle('Visualisation of OPENBCI signals widget')
#         self.win.useOpenGL()
#         # Create all the  8 plots, there title and axis values
#         for ch in range(self.N_SIGNALS):
#             self.p[ch] = self.win.addPlot(row=ch, col=0)
#             # Create plot labels
#             # self.set_plot_labels(ch)
#
#             self.data[ch] = deque(np.zeros(self.N_DATA), maxlen=self.N_DATA)
#             self.curve[ch] = self.p[ch].plot(self.data[ch])
#             # Create one update object for every channel
#             update_eeg = UpdateMultipleChPlot(self.p, self.curve, self.data)
#
#             self.update_func.append(update_eeg)
#
#             # Add the plotwidget for all channels to the window
#             plot = pg.PlotWidget()
#             self.layout.addWidget(plot, row=ch+1, col=0, rowspan=1)
#             self.timer.timeout.connect(plot, self.update_eeg_plotting)
#
#
#     def set_plot_labels(self, ch):
#         # Add axis labels
#         self.p[ch].setLabel('left', 'ch {i}'.format(i=ch))
#         if ch == 0:
#             self.p[ch].setTitle("""Electrical amplitude of the signal
#                                     for the 8 channels of the OPENBCI""")
#         if ch == self.N_SIGNALS - 1:
#             self.p[ch].setLabel('bottom', 'Time', 's')
#         self.p[ch].showGrid(x=True, y=True, alpha=0.3)
#
#     def update_eeg_plotting(self):
#         self.frequency_counter.print_freq(self.num_itt)
#         self.num_itt += 1
#
#         # if num_itt % 50 == 0:
#             # self.plot[ch].setLabel('right', '{mean_ampl:.2f} muVrms'.format(
#             #                                   mean_ampl=np.mean(one_ch_deque)))    # TODO: verifier l'unité
#         self.curve[ch].setData(one_ch_deque)
#
#
#         # # Update every single channels
#         # # for ch in range(self.N_SIGNALS):
#         #     self.update_func[ch].update_eeg(self.data_queue[ch], ch, self.num_itt)
#
#
#
#
# class FFT_graph(object):
#     def __init__(self, data_queue, win, n_data_created, layout, timer):
#         # FFT plot
#         self.win = win
#         self.data_queue = data_queue
#         self.n_data_created = n_data_created
#         self.layout = layout
#         self.timer = timer
#
#         self.N_DATA = len(self.data_queue[0])
#         self.p_freq = None
#         self.curve_freq = None
#         self.last_queue_val = []                                                # TODO: ALEXM: probably better to use a Queue or a numpy array
#         self.FFT_calculated = False
#
#         # Create the fft plot
#         self.create_fft_channel()
#
#     def create_fft_channel(self):
#         """Create a frequency plot on the side"""
#         self.p_freq = self.win.addPlot(rowspan=8, row=0, col=1)
#         self.p_freq.setLabel('bottom', 'Frequency', 'hz')
#         self.p_freq.setTitle('FFT for all channels')
#         self.p_freq.showGrid(x=True, y=True, alpha=0.5)
#         data_freq = deque(np.zeros(self.N_DATA), maxlen=self.N_DATA)
#         self.curve_freq = self.p_freq.plot(data_freq)
#         # Add the plotwidget to the window
#         plot = pg.PlotWidget()
#         self.layout.addWidget(plot, row=4, col=1, rowspan=4)
#         self.timer.timeout.connect(plot)
#
#     def update_fft_plotting(self):
#         # Calcul and plot the FFT every 40 values received
#         if self.n_data_created[0] % 40 == 0:    # TODO: ALEXM make the actualisation more constant (maybe by using a timer?)
#             ch_fft = fft(self.data_queue[0])
#             # freq = fftfreq(self.data_queue[0].shape[-1])
#             self.curve_freq.setData(abs(ch_fft[:len(ch_fft) // 2]))  # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
#
#
# class MultiChannelsPyQtGraph(FFT_graph, EEG_graph):
#     def __init__(self, data_queue, n_data_created):
#         """
#
#         """
#         self.n_data_created = n_data_created
#
#         self.data_queue = data_queue
#         self.win = pg.GraphicsWindow()
#         self.init_pyqt()
#
#         FFT_graph.__init__(self, self.data_queue, self.win, self.n_data_created,
#                            self.layout, self.timer)
#         EEG_graph.__init__(self, self.data_queue, self.win, self.layout, self.timer)
#
#     def init_pyqt(self):
#         # PyQt5 elements
#         app = pg.mkQApp()
#         self.lcheck = QtGui.QPushButton('plot local')
#         self.w1 = QtGui.QPushButton('ici')
#         # Build the layout
#         self.layout = pg.LayoutWidget()
#         self.layout.addWidget(self.lcheck)
#         self.layout.addWidget(self.w1)
#         self.layout.resize(1000, 800)
#         self.layout.show()
#         self.timer = QtCore.QTimer()
#
#     # def update_all_plots(self):
#     #     self.update_eeg_plotting()
#     #     self.update_fft_plotting()
#
#     def exec_plot(self):
#         # timer = pg.QtCore.QTimer()
#         # self.timer.timeout.connect(self.update_all_plots)
#         self.timer.start(0)
#         QtGui.QApplication.instance().exec_()
#
#
#
#
#
#
