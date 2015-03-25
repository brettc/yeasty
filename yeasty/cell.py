import logging
log = logging.getLogger("cell")
import pymunk as pm

from math import pi, asin, cos
TAU = 2 * pi
import random
from pymunk import Vec2d


class Bond(object):
    def __init__(self, sim, c1, c2, angle):
        self.sim = sim
        self.c1 = c1
        self.c2 = c2

        p11, p12, g1 = self.calc_anchor(
            c1, self.sim.parameters.attach_width, angle)
        p21, p22, g2 = self.calc_anchor(
            c2, self.sim.parameters.attach_width, TAU / 2.0)
        # self.j1 = pm.DampedSpring(c1.body, c2.body, p11, p22,
                                     # 0, STIFFNESS, DAMPING)
        # self.j2 = pm.DampedSpring(c1.body, c2.body, p12, p21,
                                     # 0, STIFFNESS, DAMPING)

        self.j1 = pm.PinJoint(c1.body, c2.body, p11, p22)
        self.j2 = pm.PinJoint(c1.body, c2.body, p12, p21)

        self.j1.distance = g1 + g2
        self.j1.distance = g1 + g2
        self.gap1 = g1

        if self.sim.parameters.max_bias > 0.0:
            self.j1.max_bias = self.sim.parameters.max_bias
            self.j2.max_bias = self.sim.parameters.max_bias
        # self.j1.max_force = max_force
        # self.j2.max_force = max_force
        if self.sim.parameters.error_bias > 0.0:
            self.j1.error_bias = self.sim.parameters.error_bias
            self.j2.error_bias = self.sim.parameters.error_bias

        self.sim.space.add(self.j1)
        self.sim.space.add(self.j2)
        self.sim.add_bond(self)
        self.check = 0

    def calc_anchor(self, c, dist, ang):
        r = c.shape.radius
        theta = asin((dist / 2.0) / r)
        p1 = Vec2d(r, 0).rotated(ang - theta)
        p2 = Vec2d(r, 0).rotated(ang + theta)
        gap = r - r * cos(theta)
        return p1, p2, gap

    def grow(self):
        # Adjust the growing anchors
        p21, p22, g2 = self.calc_anchor(self.c2,
                                        self.sim.parameters.attach_width, TAU / 2.0)
        self.gap2 = g2
        self.j1.anchr2 = p22
        self.j2.anchr2 = p21
        self.j1.distance = self.gap1 + g2
        self.j2.distance = self.gap1 + g2

    def get_stretch(self, spr):
        p1 = spr.a.local_to_world(spr.anchr1)
        p2 = spr.b.local_to_world(spr.anchr2)
        return p1.get_distance(p2)

    def break_bond(self):
        self.sim.space.remove(self.j1)
        self.sim.space.remove(self.j2)

    def check_for_breakage(self, max_distort):
        # Bullshit speedups
        # self.check += 1
        # if self.check % self.sim.parameters.check_break_every != 0:
            # return

        d1 = self.get_stretch(self.j1)
        d2 = self.get_stretch(self.j2)

        if d1 > max_distort or d2 > max_distort:
            self.break_bond()
            return True

        return False

NEVER_GROWING, DORMANT, GROWING, GROWN, BROKEN = range(5)


class Growth(object):
    def __init__(self, cell, angle, state):
        self.cell = cell
        self.angle = angle
        self.state = state
        if state == NEVER_GROWING:
            self.birth_step = None
        else:
            when = int(random.expovariate(
                1.0 / self.cell.sim.parameters.wait_till_grow))
            self.birth_step = cell.sim.time_step + when

    def step(self):
        if self.state == NEVER_GROWING:
            return
        if self.state == DORMANT:
            if self.cell.sim.time_step >= self.birth_step:
                if len(self.cell.sim.cells) < self.cell.sim.parameters.max_cells:
                    self.new_child()
        elif self.state == GROWING:
            self.grow_bond()
        elif self.state == GROWN:
            if self.cell.dead or self.child.dead:
                max_distort = self.cell.sim.parameters.max_dead_joint_distortion
            else:
                max_distort = self.cell.sim.parameters.max_joint_distortion
            if self.bond.check_for_breakage(max_distort):
                self.cell.sim.remove_bond(self.bond)
                self.state = BROKEN
                self.child.recolor(Cell.next_color, 0)
                Cell.next_color += 1
                log.debug("Breaking into clumps %d", Cell.next_color)

    def new_child(self):
        self.state = GROWING
        c = self.cell
        b = c.body
        p = Vec2d(self.cell.sim.parameters.start_size +
                  self.cell.sim.parameters.finish_size, 0).rotated(self.angle)
        p = b.local_to_world(p)
        self.child = Cell(
            c.sim, c.color, self.cell.level + 1, p, self.angle + b.angle)
        self.bond = Bond(c.sim, c, self.child, self.angle)

    def grow_bond(self):
        if self.child.shape.radius < self.cell.sim.parameters.finish_size:
            self.bond.grow()
            # l = self.bond.joint.upper
            # l += GROW_STEP
            # self.bond.joint.set_limits(0, l)
        else:
            self.state = GROWN


class Cell(object):

    next_color = 1
    next_id = 1

    def __init__(self, sim, color, level, pos, angle):
        self.sim = sim
        self.color = color
        self.level = level  # 0 = root
        self.cell_id = Cell.next_id
        self.dead = False
        self.lifetime = int(random.expovariate(
            1.0 / self.sim.parameters.life_expectancy))
        self.apoptose_step = self.sim.time_step + self.lifetime

        Cell.next_id += 1

        radius = self.sim.parameters.start_size
        body = pm.Body(*self.get_mass_moment(radius))
        body.angle = angle
        body.position = pos
        shape = pm.Circle(body, radius)

        shape.elasticity = .2
        shape.friction = .1

        self.body = body
        self.shape = shape

        self.growing = True
        self.growth = []
        self.setup_children()
        sim.add_cell(self)

    def get_mass_moment(self, r):
        mass = pi * r * r * self.sim.parameters.mass_multiplier
        moment = pm.moment_for_circle(mass, 0, r, (0, 0))
        return mass, moment

    def recolor(self, color, level):
        self.color = color
        self.level = level
        for g in self.growth:
            if g.state == GROWING or g.state == GROWN:
                g.child.recolor(color, level + 1)

    def setup_children(self):
        if random.uniform(0, 1) < self.sim.parameters.single_branch_prob:
            a = Growth(self, TAU / 11.0, DORMANT)
            b = Growth(self, -TAU / 11.0, NEVER_GROWING)
            if random.uniform(0, 1) < .5:
                self.growth = [a, b]
            else:
                self.growth = [b, a]
        else:
            a = Growth(self, TAU / 11.0, DORMANT)
            b = Growth(self, -TAU / 11.0, DORMANT)
            self.growth = [a, b]

    def step(self):
        if self.growing:
            r = self.shape.radius
            if self.shape.radius >= self.sim.parameters.finish_size:
                self.growing = False
            else:
                r += self.sim.parameters.grow_step
                self.shape.unsafe_set_radius(r)
                mass, moment = self.get_mass_moment(r)
                self.body.mass = mass
                self.body.moment = moment

        else:
            # Time for own children
            if self.sim.time_step >= self.apoptose_step:
                self.dead = True
            for g in self.growth:
                g.step()


class StartCell(Cell):
    def __init__(self, sim, color):
        Cell.__init__(self, sim, 0, color, Vec2d(0, 0), 0)

    # Special case
    def setup_children(self):
        a = Growth(self, TAU / 11.0, DORMANT)
        b = Growth(self, -TAU / 11.0, DORMANT)
        c = Growth(self, pi + TAU / 11.0, DORMANT)
        d = Growth(self, pi + -TAU / 11.0, DORMANT)
        self.growth = [a, b, c, d]
