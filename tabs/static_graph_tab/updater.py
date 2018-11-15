# --General Packages --
from functools import partial
from data_processing_pipeline.uniformize_data import uniformize_data


class Updater:
    def __init__(self, gv):
        self.gv = gv

    def connect_all(self, right_panel, left_panel, gv):
        for ch in range(gv.N_CH):
            self.s = right_panel.sliders[ch]
            self.fg = right_panel.full_graphs[ch]
            self.pg = left_panel.portion_graphs[ch]
            self.cg = left_panel.classif_graphs[ch]
            self.acg = left_panel.avg_classif_graphs[ch]

            self.connect_slider()
            self.connect_full_graph_region()
            self.connect_classif_region()
            self.connect_combo_classif_to_plot()

    def connect_slider(self):
        self.s.last_pos = 0
        self.s.valueChanged.connect(partial(self.slider_update, self.s, self.fg))

    def connect_full_graph_region(self):
        self.fg.region.sigRegionChanged.connect(
            partial(self.full_graph_region_update,
                    self.fg, self.pg, self.cg))

    def connect_classif_region(self):
        self.pg.region.sigRegionChanged.connect(
            partial(self.update_classif_region,
                self.pg, self.cg, self.acg))

    def connect_combo_classif_to_plot(self):
        self.acg.combo_classif.activated.connect(
            partial(self.update_classif_plot_w_combo_classif,
                    self.acg))

    def slider_update(self, s, fg):
        self.find_slider_pos(s)
        self.update_region_w_slider(fg.region)
        self.update_plot_range_w_slider(fg.plot, fg.x_range)

    def find_slider_pos(self, s):
        self.slider_pos = s.value()
        # Keep track of the movement of the slider between two updates
        self.delta_slider = self.slider_pos - s.last_pos
        s.last_pos = self.slider_pos

    def update_classif_region(self, pg, cg, acg):
        self.keep_region_same_range(pg.classif_region)
        self.update_region_w_region(pg, cg.region, acg, cg)

    def keep_region_same_range(self, region):
        min_r, _ = region.getRegion()
        region.setRegion([min_r, min_r + self.gv.emg_signal_len])

    def full_graph_region_update(self, fg, pg, cg):
        self.find_region_pos(fg.region)
        self.update_region_w_delta_region(pg.classif_region)
        self.update_plot_range_w_region(fg.region, cg.plot)
        self.update_plot_range_w_region(fg.region, pg.plot)

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

    def update_region_w_region(self, pg, region_follow, acg, cg):
        region_dictate = pg.classif_region
        r_right, r_left = region_dictate.getRegion()

        region_follow.setRegion([r_right, r_right])
        if acg.classified_data:
            acg.update_pos_and_avg_graph(cg.region.getRegion()[0])
            data = uniformize_data(pg.data[int(r_right):int(r_left)],
                                   self.gv.emg_signal_len)
            acg.update_classif_region_plot(data)

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

    def update_classif_plot_w_combo_classif(self, acg):
        acg.update_avg_graph_from_combo_box(acg.combo_classif.currentText())
        # t = self.pg.t[int(self.r_left): int(self.r_right)]