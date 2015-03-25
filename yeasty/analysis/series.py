import logging
log = logging.getLogger("analysis.series")

from base import ReplicateAnalysis, register_analysis

import numpy
import csv

@register_analysis
class series(ReplicateAnalysis):
    def make_series_dtype(self):
        """Make a numpy array for collecting longitudinal data
        """
        return numpy.dtype([
            # Timestep
            # ('t', numpy.int32),

            # Some data we store
            # If you add it here, you'll need to update the getters below too
            ('count', numpy.float64),
            # ('explored_by_type', numpy.float64, self.num_types)
            ])

    def begin_replicate(self, sim):
        log.info("setting up series")
        # Use the auto storage to create something permanent
        N = sim.parameters.max_steps
        self.data = numpy.zeros(N, self.make_series_dtype())

    def step(self, sim):
        # Write a per step file as well
        # log.info("at step %d", sim.time_step)
        now = self.data[sim.time_step]
        now['count'] = len(sim.cells)

    def end_replicate(self, sim):
        f = self.get_file('series.csv')

        # TODO automate this using dtypes...
        csv_writer = csv.writer(f)
        csv_writer.writerow(['step', 'count'])
        for i, row in enumerate(self.data):
            csv_writer.writerow([
                i,
                row['count'],
            ])

