# --General Packages --
from functools import partial
from data_processing_pipeline.uniformize_data import uniformize_data


class Updater:
    def __init__(self, gv):
        self.gv = gv

    def connect_all(self, right_panel, left_panel, gv):
        sliders = right_panel.sliders
        full_graphs = right_panel.full_graphs
        portion_graphs = left_panel.portion_graphs
        classif_graphs = left_panel.classif_graphs
        avg_classif_graphs = left_panel.avg_classif_graphs

        for ch in range(gv.N_CH):
            self.connect_slider(sliders[ch], full_graphs[ch])
            self.connect_full_graph_region(
                full_graphs[ch], portion_graphs[ch], classif_graphs[ch])
            self.connect_classif_region(
                portion_graphs[ch], classif_graphs[ch], avg_classif_graphs[ch])

    def connect_slider(self, slider, full_graph):
        slider.last_pos = 0
        slider.valueChanged.connect(
            partial(self.slider_update, slider, full_graph))

    def connect_full_graph_region(self, full_graph, portion_graph, classif_graph):
        full_graph.region.sigRegionChanged.connect(
            partial(self.full_graph_region_update,
                    full_graph, portion_graph, classif_graph))

    def connect_classif_region(
            self, portion_graph, classif_graph, avg_classif_graph):
        portion_graph.region.sigRegionChanged.connect(
            partial(self.update_classif_region,
                portion_graph, classif_graph, avg_classif_graph))

    def update_classif_region(self, portion_graph, classif_graph, avg_classif_graph):
        self.keep_region_same_range(portion_graph.classif_region)
        self.update_region_w_region(
            portion_graph, classif_graph.region, avg_classif_graph,
            classif_graph)

    def keep_region_same_range(self, region):
        min_r, _ = region.getRegion()
        region.setRegion([min_r, min_r + self.gv.emg_signal_len])

    def slider_update(self, slider, full_graph):
        self.find_slider_pos(slider)
        self.update_region_w_slider(full_graph.region)
        self.update_plot_range_w_slider(full_graph.plot, full_graph.x_range)

    def full_graph_region_update(self, full_graph, portion_graph, classif_graph):
        self.find_region_pos(full_graph.region)
        self.update_region_w_delta_region(portion_graph.classif_region)
        self.update_plot_range_w_region(full_graph.region, classif_graph.plot)
        self.update_plot_range_w_region(full_graph.region, portion_graph.plot)

    def find_slider_pos(self, slider):
        self.slider_pos = slider.value()
        # Keep track of the movement of the slider between two updates
        self.delta_slider = self.slider_pos - slider.last_pos
        slider.last_pos = self.slider_pos

    def find_region_pos(self, region):
        region.start_pos, _ = region.getRegion()
        self.delta_region = region.start_pos - region.last_pos
        region.last_pos = region.start_pos

    def find_full_graph_region_pos(self, region):
        self.x_min, _ = region.getRegion()
        self.delta_region = self.x_min - region.last_pos

    def update_region_w_delta_region(self, region_follow):
        r_right, r_left = region_follow.getRegion()
        region_follow.setRegion(
            [r_right + self.delta_region, r_left + self.delta_region])

    def update_region_w_region(
            self, portion_graph, region_follow, avg_classif_graph, classif_graph):
        region_dictate = portion_graph.classif_region
        r_right, r_left = region_dictate.getRegion()

        region_follow.setRegion([r_right, r_right])
        if avg_classif_graph.classified_data:
            avg_classif_graph.update_pos_and_avg_graph(
                classif_graph.region.getRegion()[0])
            print('r_left_right', r_right, r_left)
            data = uniformize_data(
                portion_graph.data[int(r_right):int(r_left)],
                self.gv.emg_signal_len)
            avg_classif_graph.update_classif_region_plot(data)

    def update_region_w_slider(self, region):
        r_right = region.boundingRect().right()
        r_left = region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        region.setRegion([r_right + self.delta_slider, r_left + self.delta_slider])

    def update_plot_range_w_slider(self, plot, x_range):
        # Update the graph range based on the slider position
        plot.setXRange(self.slider_pos, self.slider_pos + x_range)

    def update_plot_range_w_region(self, region, plot):
        """ Update the portion plot (top left) range based on the region position
           on the full graph (right)
        """
        min_x, max_x = region.getRegion()
        plot.setXRange(min_x, max_x, padding=0)

