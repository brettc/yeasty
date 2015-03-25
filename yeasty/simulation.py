import logging
log = logging.getLogger("")
import pymunk as pm
from cell import StartCell


class SimulationInterrupt(Exception):
    pass


class Simulation(object):
    def __init__(self, treatment, replicate, parameters):
        self.treatment = treatment
        self.replicate = replicate
        self.parameters = parameters

        self.space = pm.Space(iterations=self.parameters.iterations)

        # self.space = pm.Space()
        # cp.cpSpaceUseSpatialHash(self.space._space, 60, 3000)
        self.space.gravity = (0.0, 0.0)
        self.space.damping = 0.01
        self.static_body = pm.Body()
        self.mouse_body = pm.Body()

        self.cells = []
        self.bonds = set()
        self.time_step = 0

    def step(self):
        self.space.step(self.parameters.dt)
        for c in self.cells:
            c.step()

    def add_bond(self, b):
        self.bonds.add(b)

    def remove_bond(self, b):
        self.bonds.remove(b)

    def add_cell(self, c):
        self.space.add(c.body, c.shape)
        self.cells.append(c)
        log.debug("Creating Cell %d at step %d", c.cell_id, self.time_step)

    def run(self, callbacks, progress):
        if progress:
            progress.begin(self)

        StartCell(self, 0)

        for i in range(self.parameters.max_steps):
            self.step()
            if callbacks:
                for c in callbacks:
                    c(self)
            if progress:
                progress.update(self)
                while progress.paused:
                    progress.interact(self)
                if progress.running is False:
                    log.info("User interrupted simulation, ending it ...")
                    raise SimulationInterrupt
            self.time_step += 1

        if progress:
            progress.end(self)
