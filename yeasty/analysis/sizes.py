import logging
log = logging.getLogger("analysis.sizes")
from base import ExperimentAnalysis, register_analysis

import csv

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
