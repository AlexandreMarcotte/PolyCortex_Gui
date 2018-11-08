class ClassifRegionUpdate:
    def __init__(self, portion_region, classif_region, plot, classified_data,
                 char_class_type, avg_classif_curve, avg_emg_class_type):
        self.portion_region = portion_region
        self.classif_region = classif_region
        self.plot = plot
        self.classified_data = classified_data
        self.char_class_type = char_class_type
        self.avg_classif_curve = avg_classif_curve
        self.avg_emg_class_type = avg_emg_class_type

    def update_pos_and_avg_graph(self):
        # Update the average classification grap (complete left)
        r_left = self.portion_region.boundingRect().left()
        # r_right = self.portion_region.boundingRect().right()
        try:
            classified_type = self.classified_data[int(r_left)]
            html = f'{classified_type}'
            self.char_class_type.setHtml(html)
            self.avg_classif_curve.setData(self.avg_emg_class_type[classified_type])
            self.classif_region.setRegion([r_left, r_left])
        except IndexError as e:
            print(e)