import logging
log = logging.getLogger("analysis.dump")
from base import ReplicateAnalysis, register_analysis

@register_analysis
class dump(ReplicateAnalysis):

    def summarize(self, sim):
        f = self.get_file('dump.txt')

        for c in sim.cells:
            self.write_cell(f, c)

    def write_cell(self, f, c):
        f.write("id[%05d] | color[%02d] | level[%02d] |" % (c.cell_id, c.color, c.level))
        f.write("(%02.2f, %02.2f)" % (c.body.position.x, c.body.position.y))
        f.write("\n")


