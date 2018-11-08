# class FullGraph:
#     def __init__(self):
#         pass
#
#     def add_full_static_graph(self, ch):
#         # Full graph
#         self.full_ch_layouts.append(QGridLayout())
#         self.full_graph_ch_group = QGroupBox(f'ch {ch+1}')
#         self.full_graph_ch_group.setLayout(self.full_ch_layouts[ch])
#
#         # Region of selection in the 'all_data_plot'
#         self.regions.append(pg.LinearRegionItem())
#
#         # Instanciate the plot containing all the data
#         self.all_data_plots.append(pg.PlotWidget())
#         self.all_data_plots[ch].setXRange(0, self.full_graph_x_range)
#
#         # All the values open from the saved file
#         self.full_ch_layouts[ch].addWidget(self.all_data_plots[ch], ch*2+1, 0)
#         # Add these group by channel to the right side of the separation
#         self.full_graph_layout.addWidget(self.full_graph_ch_group)