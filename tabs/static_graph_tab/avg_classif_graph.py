

class AvgClassifGraph:
    def __init__(self, ch, portion_ch_layout):
        self.ch = ch
        self.classif_plots = []
        self.avg_classif_plots = []
        self.avg_classif_curves = []

        self.create_avg_classif_plot(ch)


    def create_avg_classif_plot(self, ch):
        """Instantiate the plot containing the average classification
           on all data"""
        self.avg_classif_plots.append(pg.PlotWidget())
        self.portion_ch_layouts[ch].addWidget(self.classif_plots[ch], ch*2+1, 3)
        # Add number of the current classification in the plot's right corner
        self.all_char_class_type.append(pg.TextItem(fill=(0, 0, 0), anchor=(0.5, 0)))
        self.all_char_class_type[ch].setHtml(f'0')
        self.all_char_class_type[ch].setPos(1, 1)
        self.avg_classif_plots[ch].addItem(self.all_char_class_type[ch])
        # Set plot parameters
        self.avg_classif_plots[ch].setXRange(0, self.emg_signal_len)
        self.avg_classif_plots[ch].setYRange(-1, 1)
        self.avg_classif_curves.append(
            self.avg_classif_plots[ch].plot(np.zeros(self.emg_signal_len)))