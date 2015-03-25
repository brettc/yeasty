import logging
log = logging.getLogger("analysis.sizes")
from base import ExperimentAnalysis, register_analysis

import csv

# try:
    # from rpy2.robjects.packages import importr
    # from rpy2.robjects import (
        # DataFrame, IntVector, FloatVector, StrVector, Formula)
    # import rpy2.robjects.lib.ggplot2 as g2
    # rpy = True
# except:
    # rpy = False


@register_analysis
class sizes(ExperimentAnalysis):

    def begin_experiment(self):
        # Save it to some series
        self.output_file = self.get_file('sizes.csv')
        self.csv_writer = csv.writer(self.output_file)
        self.csv_writer.writerow(['treatment', 'size'])

    def end_replicate(self, sim):
        # global rpy

        clumps = {}
        for c in sim.cells:
            cl = clumps.setdefault(c.color, set())
            cl.add(c)

        nm = sim.treatment.name
        # Now get the size
        for cl in clumps.values():
            self.csv_writer.writerow([nm, len(cl)])

        self.output_file.flush()

        # if rpy:
            # self.create_graph(treatment_name, clump_size)

    # def create_graph(self, treatment_name, clump_size):
        # fname = self.get_file_name("clumps.pdf")

        # dataf = DataFrame({
            # 'treatment': StrVector(treatment_name),
            # 'size': IntVector(clump_size)
        # })

        # grdevices = importr('grDevices')
        # grdevices.pdf(file=fname)
        # gp = g2.ggplot(dataf)

        # gp += g2.aes_string(x='size', group='treatment')
        # gp += g2.geom_area(g2.aes_string(x='size'), stat='bin')
        # gp += g2.facet_grid(Formula('. ~ treatment'))

        # gp.plot()
        # grdevices.dev_off()

        # log.info("Made a graph in '%s'", fname)
