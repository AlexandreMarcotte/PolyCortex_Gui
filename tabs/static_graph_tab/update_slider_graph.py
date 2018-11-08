class UpdateSliderGraph:
    """
    Update the position X range of the full graph on the right side based
    on the position of the slider. The portion rectangle that is contained in
    this graph is updated at the same time
    """

    def __init__(self, slider, all_data_plot, region, slider_last,
                 classif_region, portion_region, classified_pos):
        self.slider = slider
        self.all_data_plot = all_data_plot
        self.region = region
        self.slider_last = slider_last
        self.classif_region = classif_region
        self.portion_region = portion_region
        self.classified_pos = classified_pos

    def update_graph_range(self):
        v = self.slider.value()
        # Keep track of the movement of the slider between two updates
        delta_slider = v - self.slider_last
        self.slider_last = v
        # Update the graph range based on the slider position
        self.all_data_plot.setXRange(v, v + 10000)
        r_right = self.region.boundingRect().right()
        r_left = self.region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.region.setRegion([r_right + delta_slider,
                               r_left + delta_slider])

        # Classif region
        r_right = self.classif_region.boundingRect().right()
        r_left = self.classif_region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.classif_region.setRegion([r_right + delta_slider,
                                       r_left + delta_slider])
        # Portion region
        r_right = self.portion_region.boundingRect().right()
        r_left = self.portion_region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.portion_region.setRegion([r_right + delta_slider,
                                       r_left + delta_slider])